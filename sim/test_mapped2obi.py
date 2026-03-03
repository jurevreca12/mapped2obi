from forastero.io import IORole, io_suffix_style
from forastero.driver import DriverEvent
from forastero import BaseBench
from mapped.io import MappedRequestIO, MappedResponseIO, MappedControlIO
from obi.io import ObiChAIO, ObiChRIO
from cocotb_tools.runner import get_runner
from base import get_rtl_files
from base import WAVES, ASSERTIONS, LANGUAGE, RTL_DIRS

class Mapped2ObiTB(BaseBench):
    def __init__(self, dut):
        super().__init__(dut, clk=dut.clk_i, rst=dut.rstn_i, rst_active_high=False)
        mapped_req_io = MappedRequestIO(dut, "mapped_req_", IORole.RESPONDER, io_style=io_suffix_style)
        mapped_rsp_io = MappedResponseIO(dut, "mapped_rsp_", IORole.INITIATOR, io_style=io_suffix_style)
        mapped_ctrl_io = MappedControlIO(dut, "mapped_ctrl_", IORole.RESPONDER, io_style=io_suffix_style)
        obi_a_io = ObiChAIO(dut, "obi_a", IORole.INITIATOR, io_style=io_suffix_style)
        obi_r_io = ObiChRIO(dut, "obi_r", IORole.INITIATOR, io_style=io_suffix_style)


@Mapped2ObiTB.testcase(
	reset_wait_during=2,
    reset_wait_after=0,
    timeout=1000,
    shutdown_delay=1,
    shutdown_loops=1,
)
async def smoke(tb: Mapped2ObiTB, log):
	log.info("Smoke test")


if __name__ == "__main__":
    build_args = ["-Wno-fatal", "--no-stop-fail"]
    if WAVES:
        build_args += ["--trace-fst"]
    if ASSERTIONS:
        build_args += ["-DASSERTIONS"]
    runner = get_runner("verilator")
    runner.build(
        sources=get_rtl_files(LANGUAGE),
        includes=[],
        build_args=build_args,
        hdl_toplevel="mapped2obi",
        parameters={},
        always=True,
        waves=False, # we use buildargs to get fst waves (instead of vcd)
    )
    runner.test(
        hdl_toplevel="mapped2obi",
        test_module="test_mapped2obi",
    )
