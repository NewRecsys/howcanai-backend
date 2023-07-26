import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

def kobart(text):

    # text = """
    # '우리나라는 이미 위험이 대형화, 고도화, 집적화 및 복합화된 위험사회로 접어들었다. 그러나 위험을 관리할 법, 제도, 기술, 인력, 재원, 문화 등 안전관리 인프라는 아직도 취약하다.
    # 그동안 성장위주의 경제개발 정책을 펼쳐왔기 때문이다. 국가의 안전관리 분야는 크게 예방과 사후대처로 구분할 수있다. 
    # 예방단계에서 안전관리 핵심은 위험생산자가 위험을 관리하도록 하는 것이고 사후대처단계에서의 핵심은 초기의 현장대응 역량강화와 지휘통제체계의 확립이다. 
    # 현대사회에서 위험은 대부분 경제활동과정에서 창출되는 것으로 누군가에 의해 생산되는 것으로 보아야 한다. 따라서 위험을 생산하는 자에게 위험관리를 하도록 해야 한다. 
    # 즉, 예방단계에서의 위험관리란 위험생산자가 안전기준과 원칙을제대로 지키도록 하는 것이며, 이를 실현시키는 책임과 권한은 정부에게 있다. 안전관리는 상시적인 집행을 통해서만 가능하므로 이러한 기능을 할 수 있는 적절한 안전관련 정부조직이 필요하다. 
    # 지난 몇십년동안 우리나라에서 비슷한 안전사고가 반복된 것은 전략이나 계획이 없었기 때문이 아니라 이를실천하고 집행할 추진체계가 적절하지 않은 탓이 크다. 그동안 우리나라 안전관련 정부조직은 양적으로 많은 팽창을 해왔지만 국가 전체의 안전관리 철학이나 안전관리 관점에서 안전관련 정부조직을 체계적으로 설계하고 정비한 적은 거의 없다. 
    # 안전문제를 경제개발과정에서 발생되는 필요악이나 부작용정도로 인식해 왔기 때문에 안전관련 정부조직을 단편적이고 파편적으로 개편해 왔기 때문이다. 
    # 고도의 위험사회로 접어든 우리나라에서 안전은 이제 더 이상 필요악이나 경제개발과정에서 나타나는 부작용이 아니라 국민의 생명은 물론 국가의 존립에 필수적인 기본 인프라이며, 경제성장의 발판이라는 점을 인식해야 한다. 
    # 따라서 안전관련 정부조직을 거시적이고 장기적인 관점에서 재설계하고 정비하는것이 필요하다.'
    # """

    text = text.replace('\n', ' ')

    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=1024,  eos_token_id=1)
    return tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

# '1일 0 9시까지 최소 20만3220명이 코로나19에 신규 확진되어 역대 최다 기록을 갈아치웠다.'