from re import S
from aiohttp import ClientSession
import asyncio
from pykoplenti import ApiClient
import db
import logging
from datetime import datetime, timezone

HOST = "192.168.1.107"
PWD = "hVgfJIk28j9xD2EpiM13BhzJLiV9ve"

logger = logging.getLogger(__name__)

class PvGenerator:

    def __init__(self, time, input1, input2, input3, total_input) -> None:
        self.time = time
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3
        self.total_input = total_input
    
    @staticmethod
    async def read(client):
        task_pv1 = asyncio.create_task(client.get_process_data_values('devices:local:pv1',['I','U','P']))
        task_pv2 = asyncio.create_task(client.get_process_data_values('devices:local:pv2',['I','U','P']))
        task_pv3 = asyncio.create_task(client.get_process_data_values('devices:local:pv3',['I','U','P']))

        data_pv1 = await task_pv1
        data_pv2 = await task_pv2
        data_pv3 = await task_pv3
             
        input1 = Phase(
            data_pv1['devices:local:pv1']['U'].value,
            data_pv1['devices:local:pv1']['I'].value,            
            data_pv1['devices:local:pv1']['P'].value
        )  

        input2 = Phase(
            data_pv2['devices:local:pv2']['U'].value,
            data_pv2['devices:local:pv2']['I'].value,
            data_pv2['devices:local:pv2']['P'].value
        )

        input3 = Phase(
            data_pv3['devices:local:pv3']['U'].value,
            data_pv3['devices:local:pv3']['I'].value,
            data_pv3['devices:local:pv3']['P'].value
        )

        total = Phase(
            input1.voltage + input2.voltage + input3.voltage,
            input1.current + input2.current + input3.current,
            input1.power + input2.power + input3.power
        )

        return PvGenerator(None, input1, input2, input3, total)

    @db.with_cursor(write=True)
    def save(self, *args, **kwargs) -> None:
        cursor = kwargs.get("cursor")
        time = kwargs.get("time", datetime.now(timezone.utc))        
        SQL = "INSERT INTO pv_generator (time, pv1_voltage, pv1_power, pv1_current, pv2_voltage, pv2_power, pv2_current, pv3_voltage, pv3_power, pv3_current, pv_voltage, pv_power, pv_current) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (time, self.input1.voltage, self.input1.power, self.input1.current, self.input2.voltage, self.input2.power, self.input2.current, self.input3.voltage, self.input3.power, self.input3.current, self.total_input.voltage, self.total_input.power, self.total_input.current)
        cursor.execute(SQL, data)
        logger.debug("PV Generator saved")

    @staticmethod
    @db.with_cursor()
    def fetch(*args, **kwargs):
        cursor = kwargs.pop("cursor")
        cursor.execute("SELECT * FROM pv_generator;")
        pv_generators = []
        for row in cursor.fetchall():
            pv_generators.append(PvGenerator(
                row.time,
                Phase(row.pv1_voltage, row.pv1_current, row.pv1_power),
                Phase(row.pv2_voltage, row.pv2_current, row.pv2_power),
                Phase(row.pv3_voltage, row.pv3_current, row.pv3_power),
                Phase(row.pv_voltage, row.pv_current, row.pv_power)
            ))                    
        return pv_generators

    def __str__(self) -> str:
        return (
            f"PV Generator at {self.time}\n"
            f"\tInput 1:\t{self.input1}\n"
            f"\tInput 2:\t{self.input2}\n"
            f"\tInput 3:\t{self.input3}\n"
            f"\tTotal:  \t{self.total_input}"
        )

class Inverter:

    def __init__(self, time, output_power, grid_frequency, cos_phi, phase1, phase2, phase3) -> None:
        self.time = time
        self.output_power = output_power
        self.grid_frequency = grid_frequency
        self.cos_phi = cos_phi
        self.phase1 = phase1
        self.phase2 = phase2
        self.phase3 = phase3
    
    @staticmethod
    async def read(client):
        data = await client.get_process_data_values('devices:local:ac')
        
        return Inverter(
                None,
                data['devices:local:ac']['InvOut_P'].value,
                data['devices:local:ac']['Frequency'].value,
                data['devices:local:ac']['CosPhi'].value,
                Phase(
                    data['devices:local:ac']['L1_U'].value,
                    data['devices:local:ac']['L1_I'].value,
                    data['devices:local:ac']['L1_P'].value
                ),
                Phase(
                    data['devices:local:ac']['L2_U'].value,
                    data['devices:local:ac']['L2_I'].value,
                    data['devices:local:ac']['L2_P'].value
                ),
                Phase(
                    data['devices:local:ac']['L3_U'].value,
                    data['devices:local:ac']['L3_I'].value,
                    data['devices:local:ac']['L3_P'].value
                )
            )

    @db.with_cursor(write=True)
    def save(self, *args, **kwargs) -> None:
        cursor = kwargs.get("cursor")
        time = kwargs.get("time", datetime.now(timezone.utc))        
        SQL = "INSERT INTO inverter (time, output_power, grid_frequency, cos_phi, l1_voltage, l1_power, l1_current, l2_voltage, l2_power, l2_current, l3_voltage, l3_power, l3_current) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (time, self.output_power, self.grid_frequency, self.cos_phi, self.phase1.voltage, self.phase1.power, self.phase1.current, self.phase2.voltage, self.phase2.power, self.phase2.current, self.phase3.voltage, self.phase3.power, self.phase3.current)
        cursor.execute(SQL, data)
        logger.debug("Inverter saved")

    @staticmethod
    @db.with_cursor()
    def fetch(*args, **kwargs):
        cursor = kwargs.pop("cursor")
        cursor.execute("SELECT * FROM inverter;")
        inverters = []
        for row in cursor.fetchall():        
            inverters.append(Inverter(
                row.time, 
                row.output_power, 
                row.grid_frequency, 
                row.cos_phi, 
                Phase(row.l1_voltage, row.l1_current, row.l1_power), 
                Phase(row.l2_voltage, row.l2_current, row.l2_power),
                Phase(row.l3_voltage, row.l3_current, row.l3_power)
            ))            
        return inverters

    def __str__(self) -> str:
        return (
            f"Inverter at {self.time}\n"
            f"\tOutput Power: {self.output_power}"
            f"\tGrid Frequency: {self.grid_frequency}"
            f"\tCos Phi: {self.cos_phi}\n"
            f"\tPhase 1: {self.phase1}\n"
            f"\tPhase 2: {self.phase2}\n"
            f"\tPhase 3: {self.phase3}"
        )

class Phase:
    def __init__(self, voltage=0, current=0, power=0) -> None:
        # U in Volt (V)
        self.voltage = voltage
        # I in Amper (A)
        self.current = current
        # P in Watt (W)
        self.power = power

    def __str__(self) -> str:
        return (
            f"\tVoltage: {self.voltage} V"
            f"\tCurrent: {self.current} A"
            f"\tPower: {self.power} W"
        )

class HomeCosumption:
    
    def __init__(self, time, from_battery, from_pv, from_grid, total, home_p, home_own_p) -> None:
        self.time = time
        self.current_from_battery = from_battery
        self.current_from_pv = from_pv
        self.current_from_grid = from_grid
        self.current_total = total
        self.home_p = home_p# ????        
        self.home_own_p = home_own_p# ????

    @staticmethod
    async def read(client):
        data = await client.get_process_data_values('devices:local')        
        return HomeCosumption(
            None,
            data['devices:local']['HomeBat_P'].value,
            data['devices:local']['HomePv_P'].value,
            data['devices:local']['HomeGrid_P'].value,
            data['devices:local']['HomeBat_P'].value + data['devices:local']['HomePv_P'].value + data['devices:local']['HomeGrid_P'].value,
            data['devices:local']['Home_P'].value,
            data['devices:local']['HomeOwn_P'].value
        )

    @db.with_cursor(write=True)
    def save(self, *args, **kwargs) -> None:
        cursor = kwargs.get("cursor")
        time = kwargs.get("time", datetime.now(timezone.utc))        
        SQL = "INSERT INTO home_consumption (time, from_battery, from_pv, from_grid, total, home_p, home_own_p) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        data = (time, self.current_from_battery, self.current_from_pv, self.current_from_grid, self.current_total, self.home_p, self.home_own_p)
        cursor.execute(SQL, data)
        logger.debug("Home consumption saved")

    @staticmethod
    @db.with_cursor()
    def fetch(*args, **kwargs):
        cursor = kwargs.pop("cursor")
        cursor.execute("SELECT * FROM home_consumption;")
        home_consumptions = []
        for row in cursor.fetchall():
            home_consumptions.append(HomeCosumption(
                row.time,
                row.from_battery,
                row.from_pv,
                row.from_grid,
                row.total,
                row.home_p,
                row.home_own_p
            ))
        return home_consumptions

    def __str__(self) -> str:
        return (
            f"Home Consumption at {self.time}\n"
            f"\tPV: {self.current_from_pv}"
            f"\tGrid: {self.current_from_grid}"
            f"\tBattery: {self.current_from_battery}"
            f"\tTotal: {self.current_total}"
            f"\tHomeP:{self.home_p}"
            f"\tHomeOwnP:{self.home_own_p}"
        )
    
class Statistics:

    def __init__(self, statistics) -> None:
        self.statistics = statistics

    @staticmethod
    async def read(self, client):
        data = await client.get_process_data_values('scb:statistic:EnergyFlow')
        
        statistics = []
        self.statistics.append(StatisticsData('Yield',data['scb:statistic:EnergyFlow'], 'Yield'))
        self.statistics.append(StatisticsData('EnergyHomeGrid',data['scb:statistic:EnergyFlow'], 'Home consumption from grid'))
        self.statistics.append(StatisticsData('EnergyHomePv',data['scb:statistic:EnergyFlow'], 'Home consumption from PV'))
        self.statistics.append(StatisticsData('EnergyHomeBat',data['scb:statistic:EnergyFlow'], 'Home consumption from battery'))
        self.statistics.append(StatisticsData('EnergyHome',data['scb:statistic:EnergyFlow'], 'Home consumption'))
        return Statistics(statistics)


    def __str__(self) -> str:
        output = ""
        for stats in self.statistics:
            output += (f"{stats}\n")
        return output


class StatisticsData:

    def __init__(self, data_key, raw, display_name) -> None:
        self.data_key = data_key
        self.display_name = display_name
        self.day = raw['Statistic:'+self.data_key+':Day'].value
        self.month = raw['Statistic:'+self.data_key+':Month'].value
        self.year = raw['Statistic:'+self.data_key+':Year'].value
        self.total = raw['Statistic:'+self.data_key+':Total'].value

    def __str__(self) -> str:
        return (
            f"{self.display_name}:\n"
            f"\tDay: {self.day}\n"
            f"\tMonth: {self.month}\n"
            f"\tYear: {self.year}\n"
            f"\tTotal: {self.total}\n"
        )


async def async_main(read_only=False):
    async with ClientSession() as session:
        client = ApiClient(session, HOST)
        await client.login(PWD)

        read_time = datetime.now(timezone.utc)
        logger.info("Reading data from the Inverter")
        pv_generator_task = asyncio.create_task(PvGenerator.read(client))
        inverter_task = asyncio.create_task(Inverter.read(client))
        home_consumption_task = asyncio.create_task(HomeCosumption.read(client))
        #statistics.load(client)

        pv_generator = await pv_generator_task
        inverter = await inverter_task
        home_consumption = await home_consumption_task

        # left_site_power_generation = pv_generator.input1.power + pv_generator.input2.power
        # power_to_grid = inverter.output_power - home_consumption.current_total
        
        logger.debug(pv_generator)
        logger.debug(inverter)
        logger.debug(home_consumption)

        if not read_only:
            logger.info("Saving data in DB")
            pv_generator.save(time=read_time)
            home_consumption.save(time=read_time)
            inverter.save(time=read_time)

        
        # for hc in HomeCosumption.fetch():
        #     print(hc)

        # for pg in PvGenerator.fetch():
        #     print(pg)
    
        # for inv in Inverter.fetch():
        #     print(inv)        