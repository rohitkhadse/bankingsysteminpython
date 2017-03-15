class packet_tclass(object) :
    packettype = 0 
    data = [] 
    length = 0 
    sentfrom = ""
    sentto = ""

class clientdetails(object) :
###########################################################################
    transactionid = 0
    def get_tid (self):
        return self.transactionid

    def set_tid (self, value):
        self.transactionid = value

###########################################################################
    accountNo = 0

    def get_act (self):
        return self.accountNo

    def set_act (self, value):
        self.accountNo = value

###########################################################################
    balance = 0

    def get_bal (self):
        return self.balance

    def set_bal (self, value):
        self.balance = value
###########################################################################

class query(object):
###########################################################################
    qtype = " "

    def get_Qtype (self):
        return self.qtype

    def set_Qtype (self, value):
        self.qtype = value
###########################################################################
    qrytid = 0

    def get_qtid (self):
        return self.qrytid

    def set_qtid (self, value):
        self.qrytid = value
###########################################################################
    qryact = 0

    def get_qact (self):
        return self.qryact

    def set_qact (self, value):
        self.qryact = value
###########################################################################
    qrybal = 0

    def get_qbal (self):
        return self.qrybal

    def set_qbal (self, value):
        self.qrybal = value
###########################################################################

class G_area:
###########################################################################
    already_Up1 = 1

    def get_active1 (self):
        return self.already_Up1

    def set_active1 (self, value):
        self.already_Up1 = value
###########################################################################
    already_Up2 = 1

    def get_active2 (self):
        return self.already_Up2

    def set_active2 (self, value):
        self.already_Up2 = value
###########################################################################
    already_Up3 = 1

    def get_active3 (self):
        return self.already_Up3

    def set_active3 (self, value):
        self.already_Up3 = value
###########################################################################
    count1 = 0

    def get_count1 (self):
        return self.count1

    def set_count1 (self, value):
        self.count1 = value
###########################################################################
    count2 = 0

    def get_count2 (self):
        return self.count2

    def set_count2 (self, value):
        self.count2 = value
###########################################################################
    count3 = 0

    def get_count3 (self):
        return self.count3

    def set_count3 (self, value):
        self.count3 = value
###########################################################################
    server1_status = 0

    def get_status1 (self):
        return self.server1_status

    def set_status1 (self, value):
        self.server1_status = value
###########################################################################
    server2_status = 0

    def get_status2 (self):
        return self.server2_status

    def set_status2 (self, value):
        self.server2_status = value
###########################################################################
    server3_status = 0

    def get_status3 (self):
        return self.server3_status

    def set_status3 (self, value):
        self.server3_status = value
###########################################################################
    CON1 = 0

    def get_CONCT1 (self):
        return self.CON1

    def set_CONCT1 (self, value):
        self.CON1 = value

###########################################################################
    CON2 = 0

    def get_CONCT2 (self):
        return self.CON2

    def set_CONCT2 (self, value):
        self.CON2 = value
###########################################################################
    CON3 = 0

    def get_CONCT3 (self):
        return self.CON3

    def set_CONCT3 (self, value):
        self.CON3 = value
###########################################################################
    ht1 = 0

    def get_htbt1 (self):
        return self.ht1

    def set_htbt1 (self, value):
        self.ht1 = value
###########################################################################

    SHD_SEND = 0

    def get_SDSEND (self):
        return self.SHD_SEND

    def set_SDSEND (self, value):
        self.SHD_SEND = value
###########################################################################
    RESYNC_IN_PRG = 0

    def get_syncInprgserver (self):
        return self.RESYNC_IN_PRG

    def set_syncInprgserver (self, value):
        self.RESYNC_IN_PRG = value
###########################################################################
    clnt_keep_qry_cnt = 0

    def get_clnt_count (self):
        return self.clnt_keep_qry_cnt

    def set_clnt_count (self, value):
        self.clnt_keep_qry_cnt = value
###########################################################################
    display_count = 0

    def get_count (self):
        return self.display_count

    def set_count (self, value):
        self.display_count = value
###########################################################################
    display_menu = 1

    def get_menu (self):
        return self.display_menu

    def set_menu (self, value):
        self.display_menu = value


