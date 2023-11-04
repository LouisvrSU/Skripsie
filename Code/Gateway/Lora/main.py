from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from data import data_func
import time


from components import table_content
f =868
BW = 'B250'
CR = 'CR4_5'
SF = 12
PM = 8
sync_word = 0x14

# tzinfo = pytz.timezone('Africa/Johannesburg')

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        from app import live_update
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8",'ignore'))
        SN = bytes(payload).decode("utf-8",'ignore')
        rssi_value = self.get_pkt_rssi_value()
        print(rssi_value)
        # print(self.get_modem_config_1())
        data_func.db_insert((SN, time.asctime(time.localtime()), rssi_value))

        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        # update_table(page_number)
        # print(live_update())

    def start(self):
        self.set_freq = f
        self.set_sync_word = sync_word
        self.set_preamble = PM
        self.set_spreading_factor = SF
        self.set_bw = BW
        self.set_coding_rate = CR
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        print(self.get_sync_word())
        print("LoRa Started!")


def set_page_number(num):
    global page_number 
    page_number = num
    # print(page_number)
    
def get_page_number():

    # print(page_number)
    return page_number
# def Lora_Manager(value):
#     global lora

#     print("Lora_Manager")
    
#     if value == 1:
        
        
#         BOARD.setup()
    
#         BOARD.teardown()
    
#         parser = LoRaArgumentParser("Continous LoRa receiver.")        
#         lora = LoRaRcvCont(verbose=False)
#         args = parser.parse_args(lora)
#         lora.set_mode(MODE.STDBY)
#         lora.set_pa_config(pa_select=1)
#         assert(lora.get_agc_auto_on() == 1)
        
#         print("LoRa Starting...")
#         lora.start()
#         print(lora.get_sync_word())
#         print(lora.get_freq())
#         print(lora.get_pa_config())
#         lora.set_sync_word(0x12)
#         print(lora.get_sync_word())
        
#     elif value == 0:
        
#         print("LoRa Stopping...")
#         # lora.set_mode(MODE.SLEEP)
#         BOARD.teardown()
#         lora = None
#         print("LoRa Stoped!")

def Lora_Manager():
    
    print("Lora_Manager")
    

    BOARD.setup()

    parser = LoRaArgumentParser("Continous LoRa receiver.")
    
    lora = LoRaRcvCont(verbose=False)
    args = parser.parse_args(lora)

    lora.set_mode(MODE.STDBY)
    lora.set_pa_config(pa_select=1)

    print(lora)
    assert(lora.get_agc_auto_on() == 1)

    lora.start()
        