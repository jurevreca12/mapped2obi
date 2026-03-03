from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.triggers import ClockCycles

from forastero.driver import BaseDriver
from forastero.monitor import BaseMonitor

from obi.transaction import ObiChATrans, ObiChRTrans, ObiChRBackpressureTrans

class ObiChARequestDriver(BaseDriver):
    async def drive(self, transaction: ObiChATrans):
        self.io.set("addr", transaction.addr)
        self.io.set("wdata", transaction.wdata)
        self.io.set("we", transaction.we)
        self.io.set("be", transaction.be)
        self.io.set("req", 1)
        await RisingEdge(self.clk)
        while self.io.get("gnt") == 0:
            await RisingEdge(self.clk)
        self.io.set("req", 0)
        await RisingEdge(self.clk)

class ObiChRReadyDriver(BaseDriver):
    async def drive(self, transaction: ObiChRBackpressureTrans):
        self.io.set("ready", transaction.ready)
        await ClockCycles(self.clk, transaction.cycles)

class ObiChRRequestMonitor(BaseMonitor):
    async def monitor(self, capture):
        while True:
            await RisingEdge(self.clk)
            if self.rst.value == 0:
                continue
            if (self.io.get("valid") and self.io.get("ready")):
                capture(
                    ObiChRTrans(
                        rdata = self.io.get("data"),
                    )
                )
