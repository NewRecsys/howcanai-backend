import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

import os
import random
import numpy as np
import pandas as pd
from tqdm import tqdm

import transformers
from transformers import AutoModel, AutoTokenizer
from transformers import AdamWeightDecay, AdamW, get_linear_schedule_with_warmup
from adamp import AdamP
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification, TextClassificationPipeline 

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader

import pytorch_lightning as pl
from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint

tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('/opt/ml/howcanai-backend/chat/kobart')

def kobart(text):
    text = text.replace('\n', ' ')

    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=1024,  eos_token_id=1)
    return tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)


class IntentCLSModel(LightningModule):
    def __init__(self, config):
        super(IntentCLSModel, self).__init__()
        self.save_hyperparameters() # self.hparams에 config 저장됨.
        self.validation_step_outputs = []
        self.test_step_outputs = []
        
        self.config = config
        self.bert = AutoModel.from_pretrained(self.config.model)
        self.fc = nn.Linear(self.bert.config.hidden_size, self.config.n_classes)
        self.criterion = nn.CrossEntropyLoss()
            
    def forward(self, *args):
        output = self.bert(*args)
        pred = self.fc(output.pooler_output)
        
        return pred
    
    def configure_optimizers(self):
        assert self.config.optimizer in ['AdamW', 'AdamP'], 'Only AdamW, AdamP'
        
        if self.config.optimizer == 'AdamW':
            optimizer = AdamW(self.parameters(), lr=self.config.lr, eps=self.config.adam_eps)
        elif self.config.optimizer == 'AdamP':
            optimizer = AdamP(self.parameters(), lr=self.config.lr, eps=self.config.adam_eps)
            
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.config.warmup_steps,
            num_training_steps=self.trainer.estimated_stepping_batches,
        )
            
        return {'optimizer': optimizer,
                'scheduler': scheduler
                }
          
    def training_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        y = batch['label']
        y_hat = self.forward(input_ids, attention_mask)
        
        loss = self.criterion(y_hat, y)
        self.log('train_loss', loss, on_epoch=True, logger=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        y = batch['label']
        y_hat = self.forward(input_ids, attention_mask)
        
        loss = self.criterion(y_hat, y)
        output = {'loss': loss, 'batch_labels': y, 'batch_preds': y_hat}
        self.validation_step_outputs.append(output)
        return output
    
    def on_validation_epoch_end(self):
        epoch_labels = torch.cat([x['batch_labels'] for x in self.validation_step_outputs])
        epoch_preds = torch.cat([x['batch_preds'] for x in self.validation_step_outputs])
        epoch_loss = self.criterion(epoch_preds, epoch_labels)
        
        corrects = (epoch_preds.argmax(dim=1) == epoch_labels).sum().item() 
        epoch_acc = corrects / len(epoch_labels)
        self.log('val_loss', epoch_loss, on_epoch=True, logger=True)
        self.log('val_acc', epoch_acc, on_epoch=True, logger=True)
        self.validation_step_outputs.clear()
        return {'val_loss': epoch_loss, 'val_acc': epoch_acc}
    
    def test_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        y = batch['label']
        y_hat = self.forward(input_ids, attention_mask)
        
        loss = self.criterion(y_hat, y)
        output = {'loss': loss, 'batch_labels': y, 'batch_preds': y_hat}
        self.test_step_outputs.append(output)
        return output
    
    def on_test_epoch_end(self):
        epoch_labels = torch.cat([x['batch_labels'].detach().cpu() for x in self.test_step_outputs])
        epoch_preds = torch.cat([x['batch_preds'].detach().cpu() for x in self.test_step_outputs])
        # epoch_loss = self.criterion(epoch_preds, epoch_labels)
        
        acc = accuracy_score(y_true=epoch_labels, y_pred=np.argmax(epoch_preds, axis=1))
        # average micro macro weighted
        metrics = [metric(y_true=epoch_labels, y_pred=np.argmax(epoch_preds, axis=1), average='macro' )
                   for metric in (precision_score, recall_score, f1_score)]
        
        # self.log('test_loss', epoch_loss, on_epoch=True, logger=True)
        self.log('test_acc', acc, on_epoch=True, logger=True)
        self.log('test_precision', metrics[0], on_epoch=True, logger=True)
        self.log('test_recall', metrics[1], on_epoch=True, logger=True)
        self.log('test_f1', metrics[2], on_epoch=True, logger=True)
        self.test_step_outputs.clear()
        return {'test_acc': acc, 
                'test_precision': metrics[0], 'test_recall': metrics[1], 
                'test_f1': metrics[2]
                }


def intent_inference(query:str, model:str, ckpt_path:str):
    tokenizer = AutoTokenizer.from_pretrained(model)
    best_model = IntentCLSModel.load_from_checkpoint(checkpoint_path=ckpt_path, strict=False).to('cpu')
    
    category_list = ['거래 의도 (Transactional Intent) - 여행 예약 (Travel Reservations)',
                     '거래 의도 (Transactional Intent) - 예약 및 예매 (Reservations and Bookings)',
                     '거래 의도 (Transactional Intent) - 음식 주문 및 배달 (Food Ordering and Delivery)',
                     '거래 의도 (Transactional Intent) - 이벤트 티켓 예매 (Event Ticket Booking)',
                     '거래 의도 (Transactional Intent) - 제품 구매 (Product Purchase)',
                     '네비게이셔널 의도 (Navigational Intent) - 대중교통 및 지도 (Public Transportation and Maps)',
                     '네비게이셔널 의도 (Navigational Intent) - 여행 및 관광 (Travel and Tourism)',
                     '네비게이셔널 의도 (Navigational Intent) - 웹사이트/앱 검색 (Website/App Search)',
                     '네비게이셔널 의도 (Navigational Intent) - 호텔 및 숙박 (Hotels and Accommodation)',
                     '상업적 정보 조사 의도 (Commercial Intent) - 가전제품 (Electronics)',
                     '상업적 정보 조사 의도 (Commercial Intent) - 식품 및 요리 레시피 (Food and Recipe)',
                     '상업적 정보 조사 의도 (Commercial Intent) - 제품 가격 비교 (Product Price Comparison)',
                     '상업적 정보 조사 의도 (Commercial Intent) - 제품 리뷰 (Product Reviews)',
                     '상업적 정보 조사 의도 (Commercial Intent) - 패션 및 뷰티 (Fashion and Beauty)',
                     '정보 제공 의도 (Informational Intent) - 건강 및 의학 (Health and Medicine)',
                     '정보 제공 의도 (Informational Intent) - 과학 및 기술 (Science and Technology)',
                     '정보 제공 의도 (Informational Intent) - 역사 (History)',
                     '정보 제공 의도 (Informational Intent) - 인물 정보 (Biographies)',
                     '정보 제공 의도 (Informational Intent) - 일반 지식 (General Knowledge)',
                     '정보 제공 의도 (Informational Intent) - 정치, 사회, 경제 (Politics, Society, Economy)']
    
    best_model.eval()
    best_model.freeze()
    
    tokens = tokenizer.encode_plus(
            query,
            return_tensors='pt',
            max_length=32,
            padding='max_length',
            truncation=True,
            # pad_to_max_length=True,
            add_special_tokens=False
        )
    
    pred = best_model(tokens['input_ids'], tokens['attention_mask'])
    output_idx = pred.argmax().item()
    cat = category_list[output_idx]
    return cat

