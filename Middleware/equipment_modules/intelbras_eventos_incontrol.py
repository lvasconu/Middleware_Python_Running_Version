from threading import Thread
from threading import Semaphore
import requests

class FacialEventGathererThread(Thread):  # {
    def __init__(self, ip, port, username, password):
        super().__init__()
        self.ip = ip
        self.port = port
        self.url = "http://"+ip+"/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[AccessControl]"  # noqa
        self.username = username
        self.password = password
        self.events = []
        self.semaphore = Semaphore()
        self.running = False

    def get_events(self):
        try:
            self.semaphore.acquire()
            rlist = self.events.copy()
            self.events.clear()
            return rlist
        finally:
            self.semaphore.release()

    def stop(self):
        self.running = False

    def run(self):  # {
        self.running = True
        while self.running:  # {
            try:
                rval = requests.get(self.url, auth=requests.auth.HTTPDigestAuth(self.username, self.password), stream=True, timeout=60)  # noqa
            except Exception:
                continue

            empty_lines = 0
            event = {}

            for chunk in rval.iter_lines():
                if 'Content-Length: '.encode() in chunk:
                    event = {}
                    event["command"] = 0
                    event["login_id"] = 0
                    event["ipaddr"] = ''
                    event["port"] = 0
                    event["user"] = 0
                    event["user_id"] = ''
                    event["door"] = 0
                    event["time"] = ''
                    event["access_type"] = 0
                    event["status"] = 0
                    event["door_status"] = 0
                    event["card_type"] = 0
                    event["door_open_method"] = 0
                    event["card_number"] = ''
                    event["door_number"] = 1
                    event["password"] = ''
                    event["error_code"] = 0
                    event["channel_id"] = 0
                    event["reader_id"] = ''
                    event["packet_len"] = 0
                    event["packet_num"] = 0
                    event["fingerprint_info"] = ''
                    event["collect_result"] = 0
                    empty_lines = 0

                elif chunk == ''.encode():
                    empty_lines += 1
                    if empty_lines == 2:
                        empty_lines = 0

                        Facial_event = EventFacial()
                        Facial_event.pin = event['user_id']
                        Facial_event.date = datetime.datetime.fromtimestamp(event['time'], gettz("Asia/Hong_Kong"))
                        Facial_event.card_number = event['card_number']
                        Facial_event.door_number = event['door_number'] + 1
                        Facial_event.entry_exit = event['access_type']
                        Facial_event.verify_mode = event['door_open_method']
                        Facial_event.event_type = event['command']
                        Facial_event.ip = self.ip
                        Facial_event.port = self.port
                        Facial_event.user = event['user']
                        Facial_event.door = event['door']
                        Facial_event.status = event['status']
                        Facial_event.door_status = FacialDoorStatus(event['door_status']) \
                            if event['door_status'] in set(x.value for x in FacialDoorStatus) \
                            else FacialDoorStatus.UNKNOWN
                        Facial_event.card_type = event['card_type']
                        Facial_event.password = event['password']
                        Facial_event.error_code = event['error_code']

                        # append the event to the list
                        self.semaphore.acquire()
                        self.events.append(Facial_event)
                        self.semaphore.release()
                        break

                elif '='.encode() in chunk and 'Events['.encode() in chunk:
                    try:
                        rval = re.search(r'=', chunk.decode())
                    except UnicodeDecodeError:
                        rval = None

                    if rval:
                        key = chunk[:rval.span()[0]].decode()
                        value = chunk[rval.span()[1]:].decode()
                        # print('- %s: [%s]' % (key, value))

                        if 'UserID' in key:
                            event['user_id'] = int(value, 16) if value not in ['', 'admin'] else 0

                        elif 'CardName' in key:
                            event['card_name'] = value

                        elif 'CardNo' in key:
                            event['card_number'] = int(value, 16) if value != '' else 0

                        elif 'CardType' in key:
                            value = int(value) if value != '' else -1
                            event['card_type'] = FacialCardType(value) \
                                if value in set(x.value for x in FacialCardType) \
                                else FacialCardType.UNKNOWN

                        elif 'CreateTime' in key:
                            event['time'] = int(value) if value != '' else 0

                        elif 'Door' in key:
                            event['door'] = int(value) if value != '' else 0

                        elif 'ReaderID' in key:
                            event['reader_id'] = int(value) if value != '' else 0

                        elif 'ErrorCode' in key:
                            value = int(value) if value != '' else -1
                            event['error_code'] = FacialEventErrorCode(value) \
                                if value in set(x.value for x in FacialEventErrorCode) \
                                else FacialEventErrorCode.UNKNOWN

                        elif 'Method' in key:
                            value = int(value) if value != '' else -1
                            event['door_open_method'] = FacialDoorOpenMethodREST(value) \
                                if value in set(x.value for x in FacialDoorOpenMethodREST) \
                                else FacialDoorOpenMethodREST.UNKNOWN

                        elif 'Status' in key:
                            value = int(value) if value != '' else 0
                            event['status'] = FacialEventStatus(value) \
                                if value in set(x.value for x in FacialEventStatus) \
                                else FacialEventStatus.UNKNOW

                        elif 'Type' in key:
                            if value == "Entry":
                                event['access_type'] = FacialAccessType.ENTRY
                            elif value == "Exit":
                                event['access_type'] = FacialAccessType.EXIT
                            else:
                                event['access_type'] = FacialAccessType.UNKNOWN

                        elif 'UserType' in key:
                            event['user'] = int(value) if value != '' else 0

                        elif 'EventBaseInfo.Code' in key:
                            if value == 'AccessControl':
                                event['command'] = EnumFacialEvents.DH_ALARM_ACCESS_CTL_EVENT
                            else:
                                event['command'] = EnumFacialEvents.DH_UNKNOWN_EVENT

                        elif 'EventBaseInfo.Index' in key:
                            event['door_number'] = int(value) if value != '' else 0

                        else:
                            # event[key] = value
                            pass
        # }
    # }
# }