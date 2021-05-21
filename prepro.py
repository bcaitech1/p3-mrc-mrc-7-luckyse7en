import re
def remove_useless_breacket(texts):
    """
    위키피디아 전처리를 위한 함수입니다.
    괄호 내부에 의미가 없는 정보를 제거합니다.
    아무런 정보를 포함하고 있지 않다면, 괄호를 통채로 제거합니다.
    ``수학(,)`` -> ``수학``
    ``수학(數學,) -> ``수학(數學)``
    """
    bracket_pattern = re.compile(r"\((.*?)\)")
    preprocessed_text = []
    for text in texts:
        modi_text = ""
        text = text.replace("()", "")  # 수학() -> 수학
        brackets = bracket_pattern.search(text)
        if not brackets:
            if text:
                preprocessed_text.append(text)
                continue
        replace_brackets = {}
        # key: 원본 문장에서 고쳐야하는 index, value: 고쳐져야 하는 값
        # e.g. {'2,8': '(數學)','34,37': ''}
        while brackets:
            index_key = str(brackets.start()) + "," + str(brackets.end())
            bracket = text[brackets.start() + 1 : brackets.end() - 1]
            infos = bracket.split(",")
            modi_infos = []
            for info in infos:
                info = info.strip()
                if len(info) > 0:
                    modi_infos.append(info)
            if len(modi_infos) > 0:
                replace_brackets[index_key] = "(" + ", ".join(modi_infos) + ")"
            else:
                replace_brackets[index_key] = ""
            brackets = bracket_pattern.search(text, brackets.start() + 1)
        end_index = 0
        for index_key in replace_brackets.keys():
            start_index = int(index_key.split(",")[0])
            modi_text += text[end_index:start_index]
            modi_text += replace_brackets[index_key]
            end_index = int(index_key.split(",")[1])
        modi_text += text[end_index:]
        modi_text = modi_text.strip()
        if modi_text:
            preprocessed_text.append(modi_text)
    return preprocessed_text

def remove_chars(texts):
    preprocessed_text = []
    for text in texts:
        text = text.replace("\\n\\n", ". ")
        text = text.replace("\n\n", ". ")
        text = text.replace("\\n", ". ")
        text = text.replace("\n", ". ")
        text = text.replace("..", ".")
        preprocessed_text.append(text)
    return preprocessed_text

def clean_punc(texts):
    punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', '‘': '\'', "’": '\'', 
                    "“": "\"", "”": "\"", "<":"〈", ">": "〉","＜": "〈", "＞":"〉", "ㆍ": "·", "ℓ": "liter", "∼": "~", "\u200b": "", "\ufeff": "", "・": "·", "【": "[", "】": "]", "－": "-",
                    "≪": "《", "≫": "》", "\u3000": "", "∙": "·", "①": "1.", "②": "2.", "♭": "b", "⑴": "1.","③": "3.", "④": "4.", "⑤": "5.", "⑥": "6.",
                    "⑦": "7.", "⑧": "8.", "⑨": "9.", "⑩": "10.", "，": " ", "㈜": "주식회사 ", "․": "-", "®": "", "★": "", "«": "《", "»": "》", "‧": "-", "„": ",", " ,": ", ","㎏": "kg", "⅓": "1/3", "½": "1/2", "‑": "-",
                    "㎝": "cm", "＆": "&","㏊": "ha","（": "(", "）": ")", "：": ":", "  ": " ", "|u=": "", "？": "?", "⅔": "2/3", "ＭＳ":"MS", "ｍ":"m", "Ｐ": "P", "♣": "", ".¹": ".", "、": ", ", "○○": "◯◯", "○": "◯", "㎡": "m2", "□": "◯",
                    "。": ".", "⁴": "4", ",,": ",","３": "3", "１": "1", "４": "4", "５": "5", "８": "8", "―": "-", "△": "#", "．": ". ", "⋅": "·", "％":"%", "＋": "+", "⑵": "2.", "⑶": "3.", "⑷": "4.", "⑸": "5.", "⑹": "6.", "⑺": "7.", "⑻": "8.",
                    "〔": "[", "〕": "]", "₂": "2","ᐨ": "-", "㎞": "km","／": "/", "～": "~","２": "2","･": "·","¾": "3/4","Ｖ": "V","Ｒ": "R","Ｘ": "X","６": "6","㎜": "mm","▲": "#",
                    "㎚": "nm", "χ": "X", "｢": "「", "｣": "」","⇔": "-","㎐": "Hz", "\xa0": " "}

    preprocessed_text = []
    for text in texts:
        for p in punct_mapping:
            text = text.replace(p, punct_mapping[p])
        text = text.strip()
        if text:
            preprocessed_text.append(text)
    return preprocessed_text

def remove_chinese_char(texts):
    preprocessed_text = []
    for text in texts:
        text = re.sub('성작\(聖爵', '성작(聖爵)', text)
        text = re.sub('(?P<first>\()(?P<mid>[^\)]*[一-龥]+[^\)]*)(?P<end>\))', '\g<first>\g<end>', text)
        preprocessed_text.append(text)
    return preprocessed_text

def remove_japanese_char(texts):
    preprocessed_text = []
    for text in texts:
        text = re.sub('(?P<first>\()(?P<mid>[^\)]*[ぁ-ゔァ-ヴー々〆〤]+[^\)]*)(?P<end>\))', '\g<first>\g<end>', text)
        preprocessed_text.append(text)
    return preprocessed_text

def remove_hell_char(texts):
    preprocessed_text = []
    for text in texts:
        text = re.sub('틀:誰2', '', text)
        text = re.sub('\(夏に抱れて\)', '', text)
        text = re.sub('\. \.', '.', text)
        text = re.sub(r"[\+á?\xc3\xa1]", "", text)
        text = re.sub('\(天皇崩スルトキハ皇嗣即チ践祚シ祖宗ノ神器ヲ承ク\)', "", text)
        text = re.sub('\|세종', '', text)
        text = re.sub('미․중', '미·중', text)
        text = re.sub('\(男と女のお話\)', '', text)
        text = re.sub('\|1893년 11월 1일자 일기', '1893년 11월 1일자 일기', text)
        text = re.sub('\(竜ヶ崎桃子\)', '', text)
        text = re.sub('사정 ― 집안', '사정 - 집안', text)
        text = re.sub('시리우스 Ⅱ 가솔린 엔진', '시리우스 가솔린 엔진', text)
        text = re.sub('ㅕ러', '여러', text)
        text = re.sub(' \(حصروم\)', '', text)
        text = re.sub(' \(Վիրք\)', '', text)
        text = re.sub('오반조장大番組頭', '오반조장', text)
        text = re.sub('번장요닌番頭用人', '번장요닌', text)
        text = re.sub('group=주해\|', ' ', text)
        text = re.sub('  ', ' ', text)
        text = re.sub('감성적ᐨ에로스적인', '감성적-에로스적인', text)
        text = re.sub('κερalphaς/keras', 'keras', text)
        text = re.sub('οψις/opsis', 'opsis', text)
        text = re.sub('==[^==]*==[^.]*.', '', text)
        text = re.sub(' Ewwm.だが과 성. www.mrllion.com', '', text)
        text = re.sub('\|date=March 2016', '', text)
        text = re.sub('[p]+=[0-9-]+[.]*', '', text)
        text = re.sub('page=[0-9]+', '', text)
        text = re.sub('pages=[0-9]+-[0-9]+', '', text)
        text = re.sub('행위였습니다.\|', '', text)
#        text = re.sub('# 죄수복을 입지 않을 권리. # 노역에 동원되지 않을 권리. # 교육적 오락적 목적을 위해 다른 죄수들과 자유롭게 교류할 권리. # 주 1회 면회, 편지, 소포의 권리. # 시위 과정에서 상실된 감형의 완전한 복구', '1.죄수복을 입지 않을 권리. 2.노역에 동원되지 않을 권리. 3.교육적 오락적 목적을 위해 다른 죄수들과 자유롭게 교류할 권리. 4.주 1회 면회, 편지, 소포의 권리. 5.시위 과정에서 상실된 감형의 완전한 복구', text)        
        text = re.sub('（Generalplan Ost）', '(Generalplan Ost)', text)
        text = re.sub('폴란드인- 85%；벨라루스인 - 75%；우크라이나인 - 65%；', '폴란드인- 85%, 벨라루스인 - 75%, 우크라이나인 - 65%, ', text)
        text = re.sub(', Белый дом', '', text)
        text = re.sub('諸法有定性。則無因果等諸事。如偈說。 眾因緣生法 我說即是無 亦為是假名 亦是中道義 未曾有一法 不從因緣生 是故一切法 無不是空者 眾因緣生法。我說即是空。何以故。 眾緣具足和合而物生。是物屬眾因緣故無自性。 無自性故空。空亦復空。但為引導眾生故。 以假名說。離有無二邊故名為中道。 是法無性故不得言有。亦無空故不得言無。 若法有性相。則不待眾緣而有。 若不待眾緣則無法。是故無有不空法。 ', '', text)
        text = re.sub('EMI owned the Beatles\' recordings and Abbey Road Studios, so they did not deduct fees for studio time from the band\'s royalty payments during the recording and production of Sgt. Pepper.}}', '', text)
        text = re.sub('\(\|켄료쿠보우랴쿠론\}\}\)', '', text)        
        text = re.sub('나왔다.\}\}', '나왔다.', text)
#        text = re.sub('# 가죽이나 털 뿐만 아니라 주로 섬유와 직물 등의 가공되지 않은 물질로 생산. # 디자이너, 제조업자, 계약자 그 외에 의해 패션 상품 생산. # 소매영업. # 다양한 형태의 광고와 홍보.', '1. 가죽이나 털 뿐만 아니라 주로 섬유와 직물 등의 가공되지 않은 물질로 생산. 2. 디자이너, 제조업자, 계약자 그 외에 의해 패션 상품 생산. 3. 소매영업. 4. 다양한 형태의 광고와 홍보.', text)
        text = re.sub('오언 깅그리치\|제임스 멕라클란\|2006', '', text)        
        text = re.sub('\(=고첩\)들의 책동으로', '들의 책동으로', text)  
        text = re.sub('\|en\|Roger de Flor', '(Roger de Flor)', text)
        text = re.sub('인터스텔라#는', '인터스텔라는', text)
        text = re.sub('#ENDviolence', 'ENDviolence', text)
        text = re.sub('= 303고지', '303고지', text)
        text = re.sub('날짜=[0-9-]+\|', '', text)
        text = re.sub('―수성, 금성, 지구, 화성, 목성, 그리고 토성', '(수성, 금성, 지구, 화성, 목성, 토성)', text)
        text = re.sub('Alzheimer\'s disease \(AD\)\(AD\)=Alzheimer disease', 'Alzheimer disease', text)
        text = re.sub('\|윤치호\|', '', text)
        text = re.sub('\|1919년 3월 6일.', '. 1919년 3월 6일.', text)
        text = re.sub('날짜=[0-9-]+', '', text)
        text = re.sub('스타Ⅱ', '스타크래프트 Ⅱ', text)
        text = re.sub('스타크래프트: 브루드 워', '스타크래프트 브루드워', text)
        text = re.sub('#P-완전', 'P-완전', text)
        text = re.sub('엑스맨 #1이며', '엑스맨1 이며', text)
        text = re.sub('멘셰비키의 비판˙공격과 볼셰비키', '멘셰비키의 비판, 공격과 볼셰비키', text)
        text = re.sub('ㅎ뢀약이', '활약이', text)
        text = re.sub('\(· · \|갓푸쿠·셋푸쿠·하라키리·도후쿠\}\}\)', '(갓푸쿠, 셋푸쿠, 하라키리, 도후쿠)', text)
        text = re.sub('않을 겁니다." \}\}', '않을 겁니다."', text)
#        text = re.sub('# 시작하는 알레그로. # 느린 악장. # 미뉴엣 혹은 스케르초. # 알레그로나 론도', '1. 시작하는 알레그로. 2. 느린 악장. 3. 미뉴엣 혹은 스케르초. 4. 알레그로나 론도', text)
        text = re.sub('말했다." \}\}.', '말했다."', text)
#        text = re.sub('# 종족의 우상 : 사물들을 있는 그대로 보지 않고 선입견을 가지고 보려는 인간의 경향 . # 동굴의 우상 : 개인의 성격때문에 오류를 범하는 것 . # 시장의 우상 : 언어와 용법을 잘못 써서 생기는 혼동. # 극장의 우상 : 잘못된 방법과 결부된 철학 체계로 인한 해로운 영향 .', '1. 종족의 우상 : 사물들을 있는 그대로 보지 않고 선입견을 가지고 보려는 인간의 경향. 2. 동굴의 우상 : 개인의 성격때문에 오류를 범하는 것. 3. 시장의 우상 : 언어와 용법을 잘못 써서 생기는 혼동. 4. 극장의 우상 : 잘못된 방법과 결부된 철학 체계로 인한 해로운 영향.', text)
        text = re.sub(' 귀납#프랜시스 베이컨.', '', text)
#        text = re.sub('# 편견 없는 자료수집\(관찰, 실험\). # 귀납을 통한 일반화. 가설 획득. # 가설로부', '1. 편견 없는 자료수집(관찰, 실험). 2. 귀납을 통한 일반화. 가설 획득. 3. 가설로부', text)
        text = re.sub('안ㅍ으로', '안으로', text)
        text = re.sub('Z 보손0\|link=yes', 'Z0', text)
        text = re.sub(' \}\}〈/ref〉.', '', text)
        text = re.sub('龜', '\'龜\'', text)
        text = re.sub('"을 설치하였으므로 남창이라고 하며 범방산 한 줄기가 낙동강을 향하여 머리에 돌을 이고 있는 모습이 거북이와 같다.', '을 설치하였으므로 남창이라고 하며 범방산 한 줄기가 낙동강을 향하여 머리에 돌을 이고 있는 모습이 거북이와 같다."', text)
        text = re.sub('섬네일\|right\|300px\|', '', text)
        text = re.sub('18일자 \}\}', '18일자', text)
        text = re.sub('# 제', '제', text)
        text = re.sub('text=', '', text)
        text = re.sub('〈br /〉', '', text)
        text = re.sub(' \(#웹 사이트와의 연동을 참조\)', '', text)
        text = re.sub('\(1944 - 1945\)#미국을 참조.\).', '미국을 참조)', text)
        text = re.sub('\(Schiller 2003, 25-26쪽\).', '', text)
        text = re.sub(' ─ 4대강 예산이 포함되었고 이른바 날치기 통과로 논란이 되었음 ─ ', '(4대강 예산이 포함되었고 이른바 날치기 통과로 논란이 되었음)', text)
        text = re.sub(' ⁄3이닝 동안', '1/3이닝 동안', text)
        text = re.sub('\(\|젠고민슈슈기\}\}\)', '', text)
        text = re.sub('관습적ㅇ으로', '관습적으로', text)
        text = re.sub(' 섬네일\|left\|페데리코 다 몬테펠트로의 구비오 스투디올로의 모습.', '', text)
        text = re.sub('\(козаки́\|코자키; каза́ки\|카자키; 코자치; ; казакі\)', '', text)
        text = re.sub('카자흐. 카자크는', '카자크는', text)
        text = re.sub('\([ ]*듣기\)', '', text)
        text = re.sub('\(1, 680 마일\)', '(1,680 마일)', text)
        text = re.sub('[ ]*\)', ')', text)
        text = re.sub('도ー그라ー', '도그라', text)
        text = re.sub('마쓰리り\)는', '마쓰리는', text)
        text = re.sub('[^.]*〈/ref〉[^.]*.', '', text)
        text = re.sub('\[\[팩토리 걸 \(영화\)\|팩토리 걸', '팩토리 걸', text)
        text = re.sub('투발루#국토-포기-선언', '. ', text)
        text = re.sub('\{고성능 전투기 및 폭격기, 항모기동부대 및 원자력 잠수함을 보유한 미국에게 1기의 전투기로 그러한 성능을 바라는 일본의 일점호화주의 식 요구는 의미가 없었던 것이다.\}', '고성능 전투기 및 폭격기, 항모기동부대 및 원자력 잠수함을 보유한 미국에게 1기의 전투기로 그러한 성능을 바라는 일본의 일점호화주의 식 요구는 의미가 없었던 것이다.', text)
        text = re.sub('n 0.5 의 곱', 'n+0.5 의 곱', text)
        text = re.sub('2 ⁄4', '2 1/4', text)
        text = re.sub('3 ⁄4-4 인치\)의 높이의 킹', '3 3/4-4 인치)의 높이의 킹', text)
        text = re.sub('2위 팀과 8 ⁄2 경기 차', '2위 팀과 8 1/2 경기 차', text)
        text = re.sub('336 ⁄3이닝, 28승 12패', '336 2/3이닝, 28승 12패', text)
        text = re.sub('랄프\(Ralph\}"와 "노턴', '랄프(Ralph)"와 "노턴', text)
        text = re.sub('노턴\(Norton\)\(Norton\)', '노턴(Norton)', text)
        text = re.sub('C\(←카르보니움\)이고 원자번호는 6이', 'C(라틴어:카르보니움)이고 원자번호는 6이', text)
#        text = re.sub('# 아기 낳기를 원하거나, 장차 출생할 아이의 성이 무엇인가를 알고 싶어 하거나, 아기의 운명적 추이를 알고 싶어 하거나, 또는 그 아기가 장차 자기에게 어떤 영향을 줄 것인가를 궁금하게 생각할 경우. # 전혀 아기 낳기를 원하지 않았거나 잉태한 사실을 모르고 있었음에도 불구하고 우리의 잠재의식이 예감충동에 의하여 이것을 예지하는 경우. # 자기와는 직접적인 관련이 없는 타인의 경우라 하더라도 장차 출생할 아이의 잉태여부와 그 운명적 추이에 대하여 관심을 갖고 있는 경우', '1. 아기 낳기를 원하거나, 장차 출생할 아이의 성이 무엇인가를 알고 싶어 하거나, 아기의 운명적 추이를 알고 싶어 하거나, 또는 그 아기가 장차 자기에게 어떤 영향을 줄 것인가를 궁금하게 생각할 경우. 2. 전혀 아기 낳기를 원하지 않았거나 잉태한 사실을 모르고 있었음에도 불구하고 우리의 잠재의식이 예감충동에 의하여 이것을 예지하는 경우. 3. 자기와는 직접적인 관련이 없는 타인의 경우라 하더라도 장차 출생할 아이의 잉태여부와 그 운명적 추이에 대하여 관심을 갖고 있는 경우', text)
#        text = re.sub('# 시설 입장 전, 직원과 환자들이 손을 씻을 수 있는 시설에 접근할 수 있도록 보장하기. # 각 보건 시설 세면장에 비누와, 손을 닦기 위한 깨끗한 천 또는 일회용 수건 구비하기. # 조산사가 직접 환자를 조리하는 경우, 자주 손을 씻게 할 것. 이 때 비누와 물을 이용하여, 회당 적어도 20초 이상 씻을 것. 이는 새로운 조산사가 들어오기 전, 그리고 신체 검사 전 반드시 행할 것. 조산사는 신체 검사 이후 즉시, 그리고 환자가 떠난 뒤 다시 1회 손을 씻을 것. 또한 바닥 청소 및 코 풀기 또는 재채기 이후에도 반드시 행할 것. 특히 깨끗한 물을 사용할 수 없을 경우 손 세정제를 사용할 것 . # 눈, 코, 입에 손 대지 않기. # 직원과 환자 모두, 휴지나 팔꿈치로 입을 가리고 재채기를 하는 것과 이후 손을 씻도록 조언하기. # 조산사는 시설에 입장할 때마다 적어도 팔 길이 두 배 이상 사회적 거리두기를 유지하기. 신체 검사 전후 손 씻기를 한 조산사가 코로나19로 의심되거나 또는 확진 판정이 나지 않는 한, 신체 검사 및 환자 접촉은 평소대로 행할 것 . # 환자와 직원이 거쳐 간 바닥은 표백제나 다른 물질로 소독할 것. 반드시 환자들 사이의 바닥을 휴지나 깨끗한 천으로 닦고 손을 씻을 것', '1. 시설 입장 전, 직원과 환자들이 손을 씻을 수 있는 시설에 접근할 수 있도록 보장하기. 2. 각 보건 시설 세면장에 비누와, 손을 닦기 위한 깨끗한 천 또는 일회용 수건 구비하기. 3. 조산사가 직접 환자를 조리하는 경우, 자주 손을 씻게 할 것. 이 때 비누와 물을 이용하여, 회당 적어도 20초 이상 씻을 것. 이는 새로운 조산사가 들어오기 전, 그리고 신체 검사 전 반드시 행할 것. 조산사는 신체 검사 이후 즉시, 그리고 환자가 떠난 뒤 다시 1회 손을 씻을 것. 또한 바닥 청소 및 코 풀기 또는 재채기 이후에도 반드시 행할 것. 특히 깨끗한 물을 사용할 수 없을 경우 손 세정제를 사용할 것 . 4. 눈, 코, 입에 손 대지 않기. 5. 직원과 환자 모두, 휴지나 팔꿈치로 입을 가리고 재채기를 하는 것과 이후 손을 씻도록 조언하기. 6. 조산사는 시설에 입장할 때마다 적어도 팔 길이 두 배 이상 사회적 거리두기를 유지하기. 신체 검사 전후 손 씻기를 한 조산사가 코로나19로 의심되거나 또는 확진 판정이 나지 않는 한, 신체 검사 및 환자 접촉은 평소대로 행할 것 . 7. 환자와 직원이 거쳐 간 바닥은 표백제나 다른 물질로 소독할 것. 반드시 환자들 사이의 바닥을 휴지나 깨끗한 천으로 닦고 손을 씻을 것', text)
        text = re.sub('\|김수환 추기경\}\}', '', text)
        text = re.sub('group=주\|2012년과 2013년 투르 드 프랑스를 가리킨다.', '', text)
        text = re.sub('\* 1994년 : 독일 \(스페인은 당시 월드컵 우승국이 아니었다.\)〈/REF〉', '', text)
        text = re.sub('〈ref group="주"〉 1986년~1994년까지는 3개 대회 연속으로 월드컵 우승 경험이 있는 팀들이 꼭 1팀 씩 끼어 있었다. ', '', text)
        text = re.sub('\* 1986년 : 아르헨티나, 이탈리아. \* 1990년 : 우루과이 \(스페인은 당시 월드컵 우승국이 아니었다.\). ', '', text)
        text = re.sub(' {\|. \| \|}.', '', text)
#        text = re.sub('# 마르크스-레닌주의파: 이오시프', '1. 마르크스-레닌주의파: 이오시프', text)
#        text = re.sub('# 트로츠키주의파: 레온 트로츠키가 주장', '2. 트로츠키주의파: 레온 트로츠키가 주장', text)
#        text = re.sub('# 수정주의파: 1953년부터', '3. 수정주의파: 1953년부터', text)
#        text = re.sub(' # 유럽공산주의파: 선거', ' 4. 유럽공산주의파: 선거', text)
#        text = re.sub('# 시장사회주의파: 중국공산당과 베트남공산당의', '5. 시장사회주의파: 중국공산당과 베트남공산당의', text)
        text = re.sub('없어요."\}\}라고', '없어요."라고', text)
        text = re.sub('205 ⁄3이닝을', '205 2/3이닝을', text)
        text = re.sub(' ;유처리제.', '', text)
        text = re.sub('\(=판\)\(=판\)', '(=판)', text)
        text = re.sub('최종적으로 ⁄3의 표를 넘지', '최종적으로 2/3의 표를 넘지', text)
        text = re.sub('ㅌ막부에 제안했고 막부는 이를 받아 들', '막부에 제안했고 막부는 이를 받아 들', text)
        text = re.sub('ㅔ1905년 을사 보호 조약 체결', '1905년 을사 보호 조약 체결', text)
        text = re.sub('195 ⁄3이닝을 던지며 15승 10패', '195 2/3이닝을 던지며 15승 10패', text)
        text = re.sub('\(\|니혼쿄산토다이로쿠카이젠코쿠쿄기카이\}\}\)', '', text)
        text = re.sub('\(\|로쿠젠쿄\}\}\)', '', text)
        text = re.sub(' ☞ 이것은 개신교만의 주장이다', '(이것은 개신교만의 주장이다)', text)
        text = re.sub('\{\(현재는 현역 지역주둔형식-기초훈련후 바로 지역주둔 병역, 과거 1998년전 1년 각부대 병역후 지역부대 병역\)\}', '(현재는 현역 지역주둔형식-기초훈련후 바로 지역주둔 병역, 과거 1998년전 1년 각부대 병역후 지역부대 병역)', text)
        text = re.sub('\{\(1994년 폐지-이후 상근예비역제도\)\}', '(1994년 폐지-이후 상근예비역제도)', text)
        text = re.sub('었다.1989\|', '었다.', text)
#        text = re.sub('# 장치를 구동하기 위한 적절한 에너지 공급 \(예: 전기, 압축된 가스 등\). # 호흡의 타이밍 및 크기를 조절하기 위해 압력 및 유속의 형태로 이루어지는 출력. # 장치', '1. 장치를 구동하기 위한 적절한 에너지 공급 (예: 전기, 압축된 가스 등). 2. 호흡의 타이밍 및 크기를 조절하기 위해 압력 및 유속의 형태로 이루어지는 출력. 3. 장치', text)
        text = re.sub('한계 돌ㅇ파형 연구개발', '한계 돌파형 연구개발', text)
        text = re.sub('8 ⁄3 또는 33 ⁄3로 기술 데이터에, 채널 B는 66 ⁄3 또는 ', '8 1/3 또는 33 1/3로 기술 데이터에, 채널 B는 66 2/3 또는 ', text)
#        text = re.sub('# 다른 동물은 다른', '1. 다른 동물은 다른', text)
#        text = re.sub('# 비슷한 차이가 인', '2. 비슷한 차이가 인', text)
#        text = re.sub('# 동일한 인간에게도 감', '3. 동일한 인간에게도 감', text)
#        text = re.sub('# 더 나아가 물리적 변', '4. 더 나아가 물리적 변', text)
#        text = re.sub('# 게다가, 이러한 데', '5. 게다가, 이러한 데', text)
#        text = re.sub('# 객체는 오직 간', '6. 객체는 오직 간', text)
#        text = re.sub('# 이러한 개체는 색, 온도, 크기', '7. 이러한 개체는 색, 온도, 크기', text)
#        text = re.sub('# 모든 인식은 상대', '8. 모든 인식은 상대', text)
#        text = re.sub('# 우리의 인상은 관', '9. 우리의 인상은 관', text)
#        text = re.sub('# 모든 인간은 다른 법과 사회', '10. 모든 인간은 다른 법과 사회', text)        
        text = re.sub('전위당에 이ㅡ한 ', '전위당에 의한 ', text)
        text = re.sub('RG = 2, 631.2 km', 'RG = 2,631.2 km', text)
        text = re.sub(' 부여의 건국 신화\|설명=부여의 건국에 대한 전설이나 신화에 대해서는. 설명=부여족 시조 동명왕에 대한 전설이나 신화에 대해서는', '', text)
        text = re.sub('\(x\)\(x\)', '(x)', text)
        text = re.sub('\{"북경은 20년의 세월 속에서 현대 도시로 탈바꿈했고 옛 모습이라곤 찾아볼 수 없다. 변화는 내 기억을 가물거리게 했고 진실과 환상을 뒤섞어버렸다. 어느 여름이었을 것이다. 더위 속에 사람들은 자신을 드러냈고 욕망을 억제하기 힘들어했다. 여름은 영원히 지속될 것만 같았다. 태양은 계속 우릴 따라다녔고 뙤약볕은 너무 뜨거워 현기증이 날 지경이었다. 나의 찬란했던 열 여섯 시절처럼."\}.', '"북경은 20년의 세월 속에서 현대 도시로 탈바꿈했고 옛 모습이라곤 찾아볼 수 없다. 변화는 내 기억을 가물거리게 했고 진실과 환상을 뒤섞어버렸다. 어느 여름이었을 것이다. 더위 속에 사람들은 자신을 드러냈고 욕망을 억제하기 힘들어했다. 여름은 영원히 지속될 것만 같았다. 태양은 계속 우릴 따라다녔고 뙤약볕은 너무 뜨거워 현기증이 날 지경이었다. 나의 찬란했던 열 여섯 시절처럼."', text)
        text = re.sub('데요."\}\}', '데요."', text)
        text = re.sub('오사와 히데유키\|2003\|', '', text)
        text = re.sub('대장편 도라에몽 만화판▷영화 시리즈', '대장편 도라에몽 만화판(영화 시리즈)', text)
        text = re.sub('저는 제 삼촌 부부의 농장에서 곧바로 왔어요. 그래서 보시다시피 지금 전 진흙투성이의 큰 회색 헛간용 재킷을 입고 있어요. 저를 스카우트하려고 하자 저는 "필요 없어요."라고 말했어요. 하지만 그 사람들은 \(법적으로 부모의 동의가 필수였으므로\) 제 어머니의 서명을 위조했고, 결국 저를 카메라 앞에 강제로 세웠어요 \}\}', '"저는 제 삼촌 부부의 농장에서 곧바로 왔어요. 그래서 보시다시피 지금 전 진흙투성이의 큰 회색 헛간용 재킷을 입고 있어요. 저를 스카우트하려고 하자 저는 "필요 없어요."라고 말했어요. 하지만 그 사람들은 (법적으로 부모의 동의가 필수였으므로) 제 어머니의 서명을 위조했고, 결국 저를 카메라 앞에 강제로 세웠어요."', text)
        text = re.sub('\(\|사가미토라후쿄다이지신\}\}\)', '', text)
        text = re.sub('group=참고\|name=first\|', '', text)
        
        preprocessed_text.append(text)
    return preprocessed_text

def prepro(texts):
    texts = remove_chinese_char(texts)
    texts = remove_japanese_char(texts)
    texts = remove_useless_breacket(texts)
    texts = remove_chars(texts)
    texts = remove_hell_char(texts)
    texts = clean_punc(texts)
    texts = remove_chinese_char(texts)
    texts = remove_japanese_char(texts)
    texts = remove_useless_breacket(texts)
    texts = remove_chars(texts)
    texts = remove_hell_char(texts)
    texts = clean_punc(texts) 
    return texts   
