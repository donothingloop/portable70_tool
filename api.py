import portable70_pb2

# Protobuf API handler.
class API:
    cbs = {}

    def __init__(self):
        pass

    def receive(self, filter, cb):
        self.cbs[filter] = cb

    def handle(self, buf):
        try:
            buf = bytearray(buf)

            frm = portable70_pb2.Frame()
            frm.ParseFromString(buf)

            # print(frm)
            msgt = frm.WhichOneof("data")
            if msgt in self.cbs:
                self.cbs[msgt](frm)
        except Exception:
            print("Parsing failed.")
            pass

    def config(self, config):
        upd = portable70_pb2.Update()

        if config["persist"] != None:
            upd.config.persist = config["persist"]

        if config["freq"] != None:
            upd.config.frequency = int(config["freq"])

        if config["offset"] != None:
            upd.config.offset = int(config["offset"])

        if config["callsign"] != None:
            upd.config.callsign = config["callsign"]

        if config["rssiDump"] != None:
            upd.config.rssiDump = config["rssiDump"]

        print(upd)
        buf = upd.SerializeToString()
        return buf
