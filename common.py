import hashlib
import os
from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy import Index
import models
from models import WriteBaseModel
from database import SessionLocal, engine
import datetime

TEMPLATES_DIR = "templates/basic"
SERVER_TIME = datetime.datetime.now()
TIME_YMDHIS = SERVER_TIME.strftime("%Y-%m-%d %H:%M:%S")
TIME_YMD = TIME_YMDHIS[:10]
    

def hash_password(password: str):
    '''
    비밀번호를 해시화하여 반환하는 함수
    '''
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)  


def verify_password(plain_password, hashed_passwd):
    '''
    입력한 비밀번호와 해시화된 비밀번호를 비교하여 일치 여부를 반환하는 함수
    '''
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_passwd)  

# 동적 모델 캐싱: 모델이 이미 생성되었는지 확인하고, 생성되지 않았을 경우에만 새로 생성하는 방법입니다. 
# 이를 위해 간단한 전역 딕셔너리를 사용하여 이미 생성된 모델을 추적할 수 있습니다.
_created_models = {}

def dynamic_create_write_table(table_name: str, create_table: bool = False):
    '''
    WriteBaseModel 로 부터 게시판 테이블 구조를 복사하여 동적 모델로 생성하는 함수
    인수의 table_name 에서는 g6_write_ 를 제외한 테이블 이름만 입력받는다.
    Create Dynamic Write Table Model from WriteBaseModel
    '''
    # 이미 생성된 모델 반환
    if table_name in _created_models:
        return _created_models[table_name]
    
    class_name = "Write" + table_name.capitalize()
    DynamicModel = type(
        class_name, 
        (WriteBaseModel,), 
        {   
            "__tablename__": "g6_write_" + table_name,
            "__table_args__": (
                Index(f'idx_wr_num_reply_{table_name}', 'wr_num', 'wr_reply'),
                Index(f'idex_wr_is_comment_{table_name}', 'wr_is_comment'),
                {"extend_existing": True}),
        }
    )
    # 게시판 추가시 한번만 테이블 생성
    if (create_table):
        DynamicModel.__table__.create(bind=engine, checkfirst=True)
    # 생성된 모델 캐싱
    _created_models[table_name] = DynamicModel
    return DynamicModel

def get_real_client_ip(request: Request):
    '''
    클라이언트의 IP 주소를 반환하는 함수
    '''
    if 'X-Forwarded-For' in request.headers:
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    return request.remote_addr    


def session_member_key(request: Request, member: models.Member):
    '''
    세션에 저장할 회원의 고유키를 생성하여 반환하는 함수
    '''
    ss_mb_key = hashlib.md5((member.mb_datetime + get_real_client_ip(request) + request.headers.get('User-Agent')).encode()).hexdigest()
    return ss_mb_key

# 회원레벨을 SELECT 형식으로 얻음
def get_member_level_select(id: str, start: int, end: int, selected: int, event=''):
    html_code = []
    html_code.append(f'<select id="{id}" name="{id}" {event}>')
    for i in range(start, end+1):
        html_code.append(f'<option value="{i}" {"selected" if i == selected else ""}>{i}</option>')
    html_code.append('</select>')
    return ''.join(html_code)
    
# skin_gubun(new, search, connect, faq 등) 에 따른 스킨을 SELECT 형식으로 얻음
def get_skin_select(skin_gubun, id, selected, event=''):
    skin_path = TEMPLATES_DIR + f"/{skin_gubun}"
    html_code = []
    html_code.append(f'<select id="{id}" name="{id}" {event}>')
    html_code.append(f'<option value="">선택</option>')
    for skin in os.listdir(skin_path):
        if os.path.isdir(f"{skin_path}/{skin}"):
            html_code.append(f'<option value="{skin}" {"selected" if skin == selected else ""}>{skin}</option>')
    html_code.append('</select>')
    return ''.join(html_code)


# DHTML 에디터를 SELECT 형식으로 얻음
def get_editor_select(id, selected):
    html_code = []
    html_code.append(f'<select id="{id}" name="{id}">')
    if id == 'bo_select_editor':
        html_code.append(f'<option value="" {"selected" if selected == "" else ""}>기본환경설정의 에디터 사용</option>')
    else:
        html_code.append(f'<option value="">사용안함</option>')
    for editor in os.listdir("static/plugin/editor"):
        if os.path.isdir(f"static/plugin/editor/{editor}"):
            html_code.append(f'<option value="{editor}" {"selected" if editor == selected else ""}>{editor}</option>')
    html_code.append('</select>')
    return ''.join(html_code)


# 회원아이디를 SELECT 형식으로 얻음
def get_member_id_select(id, level, selected, event=''):
    db = SessionLocal()
    members = db.query(models.Member).filter(models.Member.mb_level >= level).all()
    html_code = []
    html_code.append(f'<select id="{id}" name="{id}" {event}><option value="">선택하세요</option>')
    for member in members:
        html_code.append(f'<option value="{member.mb_id}" {"selected" if member.mb_id == selected else ""}>{member.mb_id}</option>')
    html_code.append('</select>')
    return ''.join(html_code)


# # 캡챠를 SELECT 형식으로 얻음
# def get_captcha_select(id, selected=''):
#     captcha_list = ["kcaptcha", "recaptcha", "recaptcha_inv"]
#     select_options = []
#     select_options.append(f'<select id="{id}" name="{id}" required class="required">')
#     for captcha in captcha_list:
#         if captcha == selected:
#             select_options.append(f'<option value="{captcha}" selected>{captcha}</option>')
#         else:
#             select_options.append(f'<option value="{captcha}">{captcha}</option>')
#     select_options.append('</select>')
#     return ''.join(select_options)


# 필드에 저장된 값과 기본 값을 비교하여 selected 를 반환
def get_selected(field_value, value):
    if isinstance(value, int):
        return ' selected="selected"' if (int(field_value) == int(value)) else ''
    return ' selected="selected"' if (field_value == value) else ''


# function option_array_checked($option, $arr=array()){
#     $checked = '';
#     if( !is_array($arr) ){
#         $arr = explode(',', $arr);
#     }
#     if ( !empty($arr) && in_array($option, (array) $arr) ){
#         $checked = 'checked="checked"';
#     }
#     return $checked;
# }
# 위 코드를 파이썬으로 변환해줘
def option_array_checked(option, arr=[]):
    checked = ''
    if not isinstance(arr, list):
        arr = arr.split(',')
    if arr and option in arr:
        checked = 'checked="checked"'
    return checked


# // 게시판 그룹을 SELECT 형식으로 얻음
# function get_group_select($name, $selected='', $event='')
# {
#     global $g5, $is_admin, $member;

#     $sql = " select gr_id, gr_subject from {$g5['group_table']} a ";
#     if ($is_admin == "group") {
#         $sql .= " left join {$g5['member_table']} b on (b.mb_id = a.gr_admin)
#                   where b.mb_id = '{$member['mb_id']}' ";
#     }
#     $sql .= " order by a.gr_id ";

#     $result = sql_query($sql);
#     $str = "<select id=\"$name\" name=\"$name\" $event>\n";
#     for ($i=0; $row=sql_fetch_array($result); $i++) {
#         if ($i == 0) $str .= "<option value=\"\">선택</option>";
#         $str .= option_selected($row['gr_id'], $selected, $row['gr_subject']);
#     }
#     $str .= "</select>";
#     return $str;
# }
# function option_selected($value, $selected, $text='')
# {
#     if (!$text) $text = $value;
#     if ($value == $selected)
#         return "<option value=\"$value\" selected=\"selected\">$text</option>\n";
#     else
#         return "<option value=\"$value\">$text</option>\n";
# }
# php to python above code
def get_group_select(id, selected='', event=''):
    db = SessionLocal()
    groups = db.query(models.Group).order_by(models.Group.gr_id).all()
    str = f'<select id="{id}" name="{id}" {event}>\n'
    for i, group in enumerate(groups):
        if i == 0:
            str += '<option value="">선택</option>'
        str += option_selected(group.gr_id, selected, group.gr_subject)
    str += '</select>'
    return str

def option_selected(value, selected, text=''):
    if not text:
        text = value
    if value == selected:
        return f'<option value="{value}" selected="selected">{text}</option>\n'
    else:
        return f'<option value="{value}">{text}</option>\n'