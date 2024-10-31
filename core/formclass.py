import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import Form

from core.exception import AlertException
from lib.member import set_zip_code
from lib.pbkdf2 import create_hash

@dataclass
class ConfigForm:
    cf_title: str = Form(...)
    cf_admin: Optional[str] = Form(default="")
    cf_admin_email: Optional[str] = Form(default="")
    cf_admin_email_name: Optional[str] = Form(default="")
    cf_use_point: Optional[int] = Form(default=0)
    cf_login_point: Optional[int] = Form(default=0)
    cf_memo_send_point: Optional[int] = Form(default=0)
    cf_cut_name: Optional[int] = Form(default=0)
    cf_nick_modify: Optional[int] = Form(default=0)
    cf_new_del: Optional[int] = Form(default=0)
    cf_memo_del: Optional[int] = Form(default=0)
    cf_visit_del: Optional[int] = Form(default=0)
    cf_popular_del: Optional[int] = Form(default=0)
    cf_login_minutes: Optional[int] = Form(default=0)
    cf_new_rows: Optional[int] = Form(default=0)
    cf_page_rows: Optional[int] = Form(default=0)
    cf_mobile_page_rows: Optional[int] = Form(default=0)
    cf_write_pages: Optional[int] = Form(default=0)
    cf_mobile_pages: Optional[int] = Form(default=0)
    cf_new_skin: Optional[str] = Form(default="")
    cf_search_skin: Optional[str] = Form(default="")
    cf_mobile_search_skin: Optional[str] = Form(default="")
    cf_connect_skin: Optional[str] = Form(default="")
    cf_mobile_connect_skin: Optional[str] = Form(default="")
    cf_faq_skin: Optional[str] = Form(default="")
    cf_mobile_faq_skin: Optional[str] = Form(default="")
    cf_editor: Optional[str] = Form(default="")
    cf_captcha: Optional[str] = Form(default="")
    cf_captcha_mp3: Optional[str] = Form(default="")
    cf_open_modify: Optional[int] = Form(default=0)
    cf_recaptcha_site_key: Optional[str] = Form(default="")
    cf_recaptcha_secret_key: Optional[str] = Form(default="")
    cf_use_copy_log: Optional[int] = Form(default=0)
    cf_point_term: Optional[int] = Form(default=0)
    cf_possible_ip: Optional[str] = Form(default="")
    cf_intercept_ip: Optional[str] = Form(default="")
    cf_analytics: Optional[str] = Form(default="")
    cf_add_meta: Optional[str] = Form(default="")
    cf_delay_sec: Optional[int] = Form(default=0)
    cf_link_target: Optional[str] = Form(default="")
    cf_read_point: Optional[int] = Form(default=0)
    cf_write_point: Optional[int] = Form(default=0)
    cf_comment_point: Optional[int] = Form(default=0)
    cf_download_point: Optional[int] = Form(default=0)
    cf_search_part: Optional[str] = Form(default="")
    cf_image_extension: Optional[str] = Form(default="")
    cf_flash_extension: Optional[str] = Form(default="")
    cf_movie_extension: Optional[str] = Form(default="")
    cf_filter: Optional[str] = Form(default="")
    cf_member_skin: Optional[str] = Form(default="")
    cf_mobile_member_skin: Optional[str] = Form(default="")
    cf_use_homepage: Optional[int] = Form(default=0)
    cf_req_homepage: Optional[int] = Form(default=0)
    cf_use_addr: Optional[int] = Form(default=0)
    cf_req_addr: Optional[int] = Form(default=0)
    cf_use_tel: Optional[int] = Form(default=0)
    cf_req_tel: Optional[int] = Form(default=0)
    cf_use_hp: Optional[int] = Form(default=0)
    cf_req_hp: Optional[int] = Form(default=0)
    cf_use_signature: Optional[int] = Form(default=0)
    cf_req_signature: Optional[int] = Form(default=0)
    cf_use_profile: Optional[int] = Form(default=0)
    cf_req_profile: Optional[int] = Form(default=0)
    cf_register_level: Optional[int] = Form(default=0)
    cf_register_point: Optional[int] = Form(default=0)
    cf_leave_day: Optional[int] = Form(default=0)
    cf_use_member_icon: Optional[int] = Form(default=0)
    cf_icon_level: Optional[int] = Form(default=0)
    cf_member_icon_size: Optional[int] = Form(default=0)
    cf_member_icon_width: Optional[int] = Form(default=0)
    cf_member_icon_height: Optional[int] = Form(default=0)
    cf_member_img_size: Optional[int] = Form(default=0)
    cf_member_img_width: Optional[int] = Form(default=0)
    cf_member_img_height: Optional[int] = Form(default=0)
    cf_use_recommend: Optional[int] = Form(default=0)
    cf_recommend_point: Optional[int] = Form(default=0)
    cf_prohibit_id: Optional[str] = Form(default="")
    cf_prohibit_email: Optional[str] = Form(default="")
    cf_stipulation: Optional[str] = Form(default="")
    cf_privacy: Optional[str] = Form(default="")
    cf_cert_use: Optional[int] = Form(default=0)
    cf_cert_find: Optional[int] = Form(default=0)
    cf_cert_simple: Optional[str] = Form(default="")
    cf_cert_hp: Optional[str] = Form(default="")
    cf_cert_ipin: Optional[str] = Form(default="")
    cf_cert_kg_mid: Optional[str] = Form(default="")
    cf_cert_kg_cd: Optional[str] = Form(default="")
    cf_cert_kcb_cd: Optional[str] = Form(default="")
    cf_cert_kcp_cd: Optional[str] = Form(default="")
    cf_cert_limit: Optional[int] = Form(default=0)
    cf_cert_req: Optional[int] = Form(default=0)
    cf_bbs_rewrite: Optional[int] = Form(default=0)
    cf_email_use: Optional[int] = Form(default=0)
    cf_use_email_certify: Optional[int] = Form(default=0)
    cf_formmail_is_member: Optional[int] = Form(default=0)
    cf_email_wr_super_admin: Optional[int] = Form(default=0)
    cf_email_wr_group_admin: Optional[int] = Form(default=0)
    cf_email_wr_board_admin: Optional[int] = Form(default=0)
    cf_email_wr_write: Optional[int] = Form(default=0)
    cf_email_wr_comment_all: Optional[int] = Form(default=0)
    cf_email_mb_super_admin: Optional[int] = Form(default=0)
    cf_email_mb_member: Optional[int] = Form(default=0)
    cf_email_po_super_admin: Optional[int] = Form(default=0)
    cf_social_login_use: Optional[int] = Form(default=0)

    cf_naver_clientid: Optional[str] = Form(default="")
    cf_naver_secret: Optional[str] = Form(default="")
    cf_facebook_appid: Optional[str] = Form(default="")
    cf_facebook_secret: Optional[str] = Form(default="")
    cf_twitter_key: Optional[str] = Form(default="")
    cf_twitter_secret: Optional[str] = Form(default="")
    cf_google_clientid: Optional[str] = Form(default="")
    cf_google_secret: Optional[str] = Form(default="")
    cf_googl_shorturl_apikey: Optional[str] = Form(default="")
    cf_kakao_rest_key: Optional[str] = Form(default="")
    cf_kakao_js_apikey: Optional[str] = Form(default="")
    cf_kakao_client_secret: Optional[str] = Form(default="") 
    cf_payco_clientid: Optional[str] = Form(default="")
    cf_payco_secret: Optional[str] = Form(default="")
    cf_add_script: Optional[str] = Form(default="")
    cf_sms_use: Optional[str] = Form(default="")
    cf_sms_type: Optional[str] = Form(default="")
    cf_icode_id: Optional[str] = Form(default="")
    cf_icode_pw: Optional[str] = Form(default="")
    cf_icode_server_ip: Optional[str] = Form(default="")
    cf_icode_token_key: Optional[str] = Form(default="")
    cf_1_subj: Optional[str] = Form(default="")
    cf_1: Optional[str] = Form(default="")
    cf_2_subj: Optional[str] = Form(default="")
    cf_2: Optional[str] = Form(default="")
    cf_3_subj: Optional[str] = Form(default="")
    cf_3: Optional[str] = Form(default="")
    cf_4_subj: Optional[str] = Form(default="")
    cf_4: Optional[str] = Form(default="")
    cf_5_subj: Optional[str] = Form(default="")
    cf_5: Optional[str] = Form(default="")
    cf_6_subj: Optional[str] = Form(default="")
    cf_6: Optional[str] = Form(default="")
    cf_7_subj: Optional[str] = Form(default="")
    cf_7: Optional[str] = Form(default="")
    cf_8_subj: Optional[str] = Form(default="")
    cf_8: Optional[str] = Form(default="")
    cf_9_subj: Optional[str] = Form(default="")
    cf_9: Optional[str] = Form(default="")
    cf_10_subj: Optional[str] = Form(default="")
    cf_10: Optional[str] = Form(default="")


@dataclass
class MemberForm:
    """회원 정보 기본 폼 데이터"""
    mb_password: str = Form(None)
    mb_nick: str = Form(None)
    mb_email: Optional[str] = Form(default="")
    mb_homepage: Optional[str] = Form(default="")
    mb_sex: Optional[str] = Form(default="")
    mb_recommend: Optional[str] = Form(default="")
    mb_hp: Optional[str] = Form(default="")
    mb_tel: Optional[str] = Form(default="")
    mb_certify: Optional[str] = Form(default="")
    mb_adult: Optional[int] = Form(default=0)
    mb_addr_jibeon: Optional[str] = Form(default="")
    mb_zip: Optional[str] = Form(default="")
    mb_zip1: Optional[str] = Form(default="")
    mb_zip2: Optional[str] = Form(default="")
    mb_addr1: Optional[str] = Form(default="")
    mb_addr2: Optional[str] = Form(default="")
    mb_addr3: Optional[str] = Form(default="")
    mb_mailling: Optional[int] = Form(default=0)
    mb_sms: Optional[int] = Form(default=0)
    mb_open: Optional[int] = Form(default=0)
    mb_signature: Optional[str] = Form(default="")
    mb_profile: Optional[str] = Form(default="")
    mb_memo: Optional[str] = Form(default="")
    mb_1: Optional[str] = Form(default="")
    mb_2: Optional[str] = Form(default="")
    mb_3: Optional[str] = Form(default="")
    mb_4: Optional[str] = Form(default="")
    mb_5: Optional[str] = Form(default="")
    mb_6: Optional[str] = Form(default="")
    mb_7: Optional[str] = Form(default="")
    mb_8: Optional[str] = Form(default="")
    mb_9: Optional[str] = Form(default="")
    mb_10: Optional[str] = Form(default="")


    def __post_init__(self) -> None:
        # 우편번호 분리
        self.mb_zip1, self.mb_zip2 = set_zip_code(self.mb_zip)

        # 성별
        if self.mb_sex not in {"m", "f"}:
            self.mb_sex = ""
        # 본인인증 및 성인인증 여부 체크
        if not self.mb_certify:
            self.mb_adult = 0

        # 필요없는 변수 삭제
        del self.mb_zip

@dataclass
class AdminMemberForm(MemberForm):
    """관리자 회원 정보 등록/수정 폼 데이터"""
    mb_name: str = Form(None)
    mb_level: int = Form(default=1)
    mb_intercept_date: str = Form(default="")
    mb_leave_date: str = Form(default="")

    def __post_init__(self) -> None:
        # 회원 이름 검사
        if not self.mb_name:
            raise AlertException("이름을 입력해 주세요.", 400)

        # 비밀번호 암호화
        if self.mb_password:
            self.mb_password = create_hash(self.mb_password)
        else:
            del self.mb_password

        super().__post_init__()


@dataclass
class RegisterMemberForm(MemberForm):
    """회원 가입 폼 데이터"""
    mb_id: str = Form(None)
    mb_name: str = Form(None)
    mb_password_re: str = Form(None)

    def __post_init__(self) -> None:
        # 회원 아이디 검사
        if len(self.mb_id) < 3 or len(self.mb_id) > 20:
            raise AlertException("회원아이디는 3~20자로 입력해주세요.", 400)
        if not re.match(r"^[a-zA-Z0-9_]+$", self.mb_id):
            raise AlertException("회원아이디는 영문자, 숫자, _ 만 사용할 수 있습니다.", 400)

        # 비밀번호 검사
        if not (self.mb_password and self.mb_password_re):
            raise AlertException("비밀번호를 입력해 주세요.", 400)
        if len(self.mb_password) < 4 or len(self.mb_password) > 20:
            raise AlertException("비밀번호는 4~20자로 입력해 주세요.", 400)
        if self.mb_password != self.mb_password_re:
            raise AlertException("비밀번호와 비밀번호 확인이 일치하지 않습니다.", 400)

        if not self.mb_nick:
            raise AlertException("닉네임을 입력해 주세요.", 400)

        if not self.mb_name:
            raise AlertException("이름을 입력해 주세요.", 400)

        if not self.mb_email:
            raise AlertException("이메일을 입력해 주세요.", 400)

        # 비밀번호 암호화
        self.mb_password = create_hash(self.mb_password)

        del self.mb_password_re

        super().__post_init__()


@dataclass
class UpdateMemberForm(MemberForm):
    """회원 정보 수정 폼 데이터"""
    mb_nick_date: datetime = datetime.now()
    mb_open_date: datetime = datetime.now()
    mb_password_re: str = Form(None)

    def __post_init__(self) -> None:
        # 비밀번호 변경
        if self.mb_password and self.mb_password_re:
            if len(self.mb_password) < 4 or len(self.mb_password) > 20:
                raise AlertException("비밀번호는 4~20자로 입력해주세요.", 400)

            if self.mb_password != self.mb_password_re:
                raise AlertException("비밀번호와 비밀번호 확인이 일치하지 않습니다.", 400)
            self.mb_password = create_hash(self.mb_password)
        else:
            del self.mb_password

        del self.mb_password_re

        super().__post_init__()


@dataclass
class BoardForm:
    gr_id: str = Form(...)
    bo_subject: str = Form(...)
    bo_device: str = Form(...)
    bo_mobile_subject: Optional[str] = Form(default="")
    bo_admin: Optional[str] = Form(default="")
    bo_category_list: Optional[str] = Form(default="")
    bo_use_category: Optional[int] = Form(default=0)
    bo_list_level: Optional[int] = Form(default=0)
    bo_read_level: Optional[int] = Form(default=0)
    bo_write_level: Optional[int] = Form(default=0)
    bo_reply_level: Optional[int] = Form(default=0)
    bo_comment_level: Optional[int] = Form(default=0)
    bo_upload_level: Optional[int] = Form(default=0)
    bo_download_level: Optional[int] = Form(default=0)
    bo_html_level: Optional[int] = Form(default=0)
    bo_link_level: Optional[int] = Form(default=0)
    bo_count_delete: Optional[int] = Form(default=0)
    bo_count_modify: Optional[int] = Form(default=0)
    bo_read_point: Optional[int] = Form(default=0)
    bo_write_point: Optional[int] = Form(default=0)
    bo_comment_point: Optional[int] = Form(default=0)
    bo_download_point: Optional[int] = Form(default=0)
    bo_use_sideview: Optional[int] = Form(default=0)
    bo_use_file_content: Optional[int] = Form(default=0)
    bo_use_secret: Optional[int] = Form(default=0)
    bo_use_dhtml_editor: Optional[int] = Form(default=0)
    bo_select_editor: Optional[str] = Form(default="")
    bo_use_rss_view: Optional[int] = Form(default=0)
    bo_use_good: Optional[int] = Form(default=0)
    bo_use_nogood: Optional[int] = Form(default=0)
    bo_use_name: Optional[int] = Form(default=0)
    bo_use_signature: Optional[int] = Form(default=0)
    bo_use_ip_view: Optional[int] = Form(default=0)
    bo_use_list_view: Optional[int] = Form(default=0)
    bo_use_list_file: Optional[int] = Form(default=0)
    bo_use_list_content: Optional[int] = Form(default=0)
    bo_table_width: Optional[int] = Form(default=0)
    bo_subject_len: Optional[int] = Form(default=0)
    bo_mobile_subject_len: Optional[int] = Form(default=0)
    bo_page_rows: Optional[int] = Form(default=0)
    bo_mobile_page_rows: Optional[int] = Form(default=0)
    bo_new: Optional[int] = Form(default=0)
    bo_hot: Optional[int] = Form(default=0)
    bo_image_width: Optional[int] = Form(default=0)
    bo_skin: Optional[str] = Form(default="")
    bo_mobile_skin: Optional[str] = Form(default="")
    bo_include_head: Optional[str] = Form(default="")
    bo_include_tail: Optional[str] = Form(default="")
    bo_content_head: Optional[str] = Form(default="")
    bo_mobile_content_head: Optional[str] = Form(default="")
    bo_content_tail: Optional[str] = Form(default="")
    bo_mobile_content_tail: Optional[str] = Form(default="")
    bo_insert_content: Optional[str] = Form(default="")
    bo_gallery_cols: Optional[int] = Form(default=0)
    bo_gallery_width: Optional[int] = Form(default=0)
    bo_gallery_height: Optional[int] = Form(default=0)
    bo_mobile_gallery_width: Optional[int] = Form(default=0)
    bo_mobile_gallery_height: Optional[int] = Form(default=0)
    bo_upload_size: Optional[int] = Form(default=0)
    bo_reply_order: Optional[int] = Form(default=0)
    bo_use_search: Optional[int] = Form(default=0)
    bo_order: Optional[int] = Form(default=0)
    bo_count_write: Optional[int] = Form(default=0)
    bo_count_comment: Optional[int] = Form(default=0)
    bo_write_min: Optional[int] = Form(default=0)
    bo_comment_min: Optional[int] = Form(default=0)
    bo_write_max: Optional[int] = Form(default=0)
    bo_comment_max: Optional[int] = Form(default=0)
    # bo_notice: Optional[int] = Form(default=0)
    bo_upload_count: Optional[int] = Form(default=0)
    bo_use_email: Optional[int] = Form(default=0)
    bo_use_cert: Optional[str] = Form(default="")
    bo_use_sns: Optional[int] = Form(default=0)
    bo_use_captcha: Optional[int] = Form(default=0)
    bo_sort_field: Optional[str] = Form(default="")
    bo_1_subj: Optional[str] = Form(default="")
    bo_2_subj: Optional[str] = Form(default="")
    bo_3_subj: Optional[str] = Form(default="")
    bo_4_subj: Optional[str] = Form(default="")
    bo_5_subj: Optional[str] = Form(default="")
    bo_6_subj: Optional[str] = Form(default="")
    bo_7_subj: Optional[str] = Form(default="")
    bo_8_subj: Optional[str] = Form(default="")
    bo_9_subj: Optional[str] = Form(default="")
    bo_10_subj: Optional[str] = Form(default="")
    bo_1: Optional[str] = Form(default="")
    bo_2: Optional[str] = Form(default="")
    bo_3: Optional[str] = Form(default="")
    bo_4: Optional[str] = Form(default="")
    bo_5: Optional[str] = Form(default="")
    bo_6: Optional[str] = Form(default="")
    bo_7: Optional[str] = Form(default="")
    bo_8: Optional[str] = Form(default="")
    bo_9: Optional[str] = Form(default="")
    bo_10: Optional[str] = Form(default="")


@dataclass
class GroupForm:
    gr_subject: str = Form(...)
    gr_device: Optional[str] = Form(default="")
    gr_admin: Optional[str] = Form(default="")
    gr_use_access: Optional[int] = Form(default=0)
    gr_1_subj: Optional[str] = Form(default="")
    gr_2_subj: Optional[str] = Form(default="")
    gr_3_subj: Optional[str] = Form(default="")
    gr_4_subj: Optional[str] = Form(default="")
    gr_5_subj: Optional[str] = Form(default="")
    gr_6_subj: Optional[str] = Form(default="")
    gr_7_subj: Optional[str] = Form(default="")
    gr_8_subj: Optional[str] = Form(default="")
    gr_9_subj: Optional[str] = Form(default="")
    gr_10_subj: Optional[str] = Form(default="")
    gr_1: Optional[str] = Form(default="")
    gr_2: Optional[str] = Form(default="")
    gr_3: Optional[str] = Form(default="")
    gr_4: Optional[str] = Form(default="")
    gr_5: Optional[str] = Form(default="")
    gr_6: Optional[str] = Form(default="")
    gr_7: Optional[str] = Form(default="")
    gr_8: Optional[str] = Form(default="")
    gr_9: Optional[str] = Form(default="")
    gr_10: Optional[str] = Form(default="")


@dataclass
class WriteForm:
    ca_name: str = Form(None)
    wr_name: str = Form(None)
    wr_email: str = Form(None)
    wr_homepage: str = Form(None)
    wr_password: str = Form(None)
    wr_subject: str = Form(...)
    wr_content: str = Form("")
    wr_is_comment: int = 0
    wr_link1: str = Form(None)
    wr_link2: str = Form(None)

    wr_1: str = Form("")
    wr_2: str = Form("")
    wr_3: str = Form("")
    wr_4: str = Form("")
    wr_5: str = Form("")
    wr_6: str = Form("")
    wr_7: str = Form("")
    wr_8: str = Form("")
    wr_9: str = Form("")
    wr_10: str = Form("")


@dataclass
class WriteCommentForm:
    w: str = Form(...)
    wr_id: int = Form(...)
    wr_content: str = Form(...)
    wr_name: str = Form(None)
    wr_password: str = Form(None)
    wr_secret: str = Form(None)
    comment_id: int = Form(default=0)


@dataclass
class ContentForm:
    co_subject: str = Form(...)
    co_content: str = Form(default="")
    co_mobile_content: str = Form(default="")
    co_html: str = Form(default="1")
    co_skin: str = Form(default="")
    co_mobile_skin: str = Form(default="")


@dataclass
class FaqMasterForm:
    fm_subject: str = Form(...)
    fm_head_html: str = Form(default="")
    fm_tail_html: str = Form(default="")
    fm_mobile_head_html: str = Form(default="")
    fm_mobile_tail_html: str = Form(default="")
    fm_order: int = Form(default=0)


@dataclass
class FaqForm:
    fa_subject: str = Form(default="")
    fa_content: str = Form(default="")
    fa_order: int = Form(default=1)

@dataclass
class PollForm:
    po_subject: str = Form(...)
    po_poll1: str = Form(...)
    po_poll2: str = Form(...)
    po_poll3: str = Form(None)
    po_poll4: str = Form(None)
    po_poll5: str = Form(None)
    po_poll6: str = Form(None)
    po_poll7: str = Form(None)
    po_poll8: str = Form(None)
    po_poll9: str = Form(None)
    po_cnt1: int = Form(None)
    po_cnt2: int = Form(None)
    po_cnt3: int = Form(None)
    po_cnt4: int = Form(None)
    po_cnt5: int = Form(None)
    po_cnt6: int = Form(None)
    po_cnt7: int = Form(None)
    po_cnt8: int = Form(None)
    po_cnt9: int = Form(None)
    po_etc: str = Form(None)
    po_level: int = Form(None)
    po_point: int = Form(default=0)
    po_use: int = Form(None)


@dataclass
class AutoSaveForm:
    as_uid: Optional[int] = Form(default=0)
    as_subject: str = Form(default="")
    as_content: str = Form(default="")
    as_datetime: datetime = Form(default=datetime.now())

      
@dataclass
class QaConfigForm:
    """1:1문의 설정 폼 데이터
    - 더이상 사용하지 않는 기능 (변수)
        1. 상단 파일 경로 (qa_include_head)
        2. 하단 파일 경로 (qa_include_tail)
    """
    qa_title: str = Form(...)
    qa_category: str = Form(None)
    qa_skin: str = Form(default="")
    qa_mobile_skin: str = Form(default="")
    qa_use_email: int = Form(0)
    qa_req_email: int = Form(0)
    qa_use_hp: int = Form(0)
    qa_req_hp: int = Form(0)
    qa_use_sms: int = Form(None)
    qa_send_number: str = Form(None)
    qa_admin_hp: str = Form("")
    qa_admin_email: str = Form("")
    qa_use_editor: int = Form(None)
    qa_subject_len: int = Form(None)
    qa_mobile_subject_len: int = Form(None)
    qa_page_rows: int = Form(None)
    qa_mobile_page_rows: int = Form(None)
    qa_image_width: int = Form(None)
    qa_upload_size: int = Form(None)
    qa_insert_content: str = Form("")
    qa_include_head: str = Form(None)
    qa_include_tail: str = Form(None)
    qa_content_head: str = Form("")
    qa_content_tail: str = Form("")
    qa_mobile_content_head: str = Form("")
    qa_mobile_content_tail: str = Form("")
    qa_1_subj: str = Form(None)
    qa_2_subj: str = Form(None)
    qa_3_subj: str = Form(None)
    qa_4_subj: str = Form(None)
    qa_5_subj: str = Form(None)
    qa_1: str = Form(None)
    qa_2: str = Form(None)
    qa_3: str = Form(None)
    qa_4: str = Form(None)
    qa_5: str = Form(None)


@dataclass
class QaContentForm:
    """
    1:1문의 폼 데이터
    """
    qa_email: str = Form("")
    qa_hp: str = Form("")
    qa_category: str = Form(None)
    qa_email_recv: int = Form(0)
    qa_sms_recv: int = Form(0)
    qa_html: int = Form(None)
    qa_subject: str = Form(...)
    qa_content: str = Form("")

    qa_1: str = Form("")
    qa_2: str = Form("")
    qa_3: str = Form("")
    qa_4: str = Form("")
    qa_5: str = Form("")


@dataclass
class NewwinForm:
    """
    팝업 폼 데이터
    """
    nw_division: str = Form(...)
    nw_device: str = Form(...)
    nw_begin_time: datetime = Form(...)
    nw_end_time: datetime = Form(...)
    nw_disable_hours: int = Form(...)
    nw_left: int = Form(...)
    nw_top: int = Form(...)
    nw_height: int = Form(...)
    nw_width: int = Form(...)
    nw_subject: str = Form(...)
    nw_content: str = Form(...)
    nw_content_html: int = Form(0)

@dataclass
class SocialProfile:
    """소셜 프로필 폼 데이터"""
    mb_id: str
    provider: str
    identifier: str
    profile_url: str
    photourl: str
    displayname: str
    disciption: str

@dataclass
class InstallFrom:
    db_engine: str = Form(...)
    db_host: str = Form("")
    db_port: int = Form(0)
    db_user: str = Form("")
    db_password: str = Form("")
    db_name: str = Form("")
    db_table_prefix: str = Form(...)

    admin_id: str = Form(...)
    admin_password: str = Form(...)
    admin_name: str = Form(...)
    admin_email: str = Form(...)

    reinstall: int = Form(None)
    is_skip_admin: int = Form(None)
