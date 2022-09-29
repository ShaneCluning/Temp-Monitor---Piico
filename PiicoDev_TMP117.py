from PiicoDev_MachineOnly import *

REG_TEMPC = 0x00
_baseAddr = 0x48
compat_str = "\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n"


class PiicoDev_TMP117(object):
    def __init__(
        self, bus=None, freq=None, sda=None, scl=None, address=_baseAddr, asw=None
    ):
        if type(asw) is list:
            assert (
                max(asw) <= 1 and min(asw) >= 0 and len(asw) is 4
            ), "asw must be a list of 1/0, length=4"
            self.addr = _baseAddr + 1 * asw[1] + 2 * asw[2] + 3 * asw[3]
            print(self.addr)
        else:
            self.addr = address
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        print(
            "Creating i2C: Bus: %s, Freq: %s, sda: %s, scl: %s"
            % (str(bus), str(freq), str(sda), str(scl))
        )
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)

    def readTempC(self):
        try:
            data = self.i2c.readfrom_mem(self.addr, REG_TEMPC, 2)
        except:
            print(i2c_err_str.format(self.addr))
            return float("NaN")

        tempDataRaw = int.from_bytes(data, "big")
        if tempDataRaw >= 0x8000:
            return -256.0 + (tempDataRaw - 0x8000) * 7.8125e-3
        else:
            return tempDataRaw * 7.8125e-3
