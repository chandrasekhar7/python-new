"""
db_model.py: Database Schema and Interaction for Leakware

This file utilizes SQLAlchemy, a powerful Object Relational Mapper (ORM), to define the
structure of Leakware's database and provide an intuitive Python interface for interaction.

Key Benefits of using SQLAlchemy:
- Mapping: SQLAlchemy maps Python classes (e.g., Leakware, Measurements) to database tables,
  streamlining data storage and retrieval without needing to write raw SQL queries for
  most operations.
- Abstraction: Working with database entities feels natural using Python objects. SQLAlchemy handles
  database-specific syntax, improving code readability and maintainability. SQLAlchemy also enables
  switching between database types (SQLite, MySQL, PostgreSQL) with minimal code changes.
- Relationships: Easily define and navigate relationships between test sessions, measurements,
and other data.

Key Classes:
- Base: Acts as the foundation for all database models.
- TimestampMixin: Provides 'created_at' and 'updated_at' columns for automatic timestamp tracking.
- Leakware: Represents a single leak test session, acting as the central point connecting
other information.
- DataInformation: Stores metadata associated with a leak test session, including project
details and test notes.
- PemSpecificElements: Stores PEM-specific elements for a leak test session.
- Measurements: Stores individual measurement readings taken during a leak test session.
- Specimens: Stores X & Y coordinate data likely related to the location of a leak or
specific measurement points.
- Devices: Stores configuration for devices, likely related to serial communication.
- Report: Stores test images, the type of test medium, and notes for a leak test session.
- MassFlowSensorData: Stores values received from the Mass Flow Controller.
- HeliumAnalyzerData: Stores values received from the Helium Analyzer.
- PressureGaugeData: Stores values received from the Pressure Gauge.

Dependencies:
- sqlalchemy

Usage:
This module is typically imported and used throughout the application to interact with the database,
create and retrieve data models, and define relationships between entities.
"""

# -----------------------------------------------------
# Import Necessary Modules
# -----------------------------------------------------
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
    ForeignKey, JSON, Float, Boolean, func
from sqlalchemy.orm import relationship, sessionmaker, DeclarativeBase

# Data base connection
engine = create_engine("sqlite:///leak_ware_db.db")
Session = sessionmaker(bind=engine)

# --- Base Class for Common Behavior ---
class Base(DeclarativeBase):
    """
    Acts as the foundation for all database models. SQLAlchemy will use this 
    to generate appropriate table structures. 
    """

class TimestampMixin:
    """
    Provides 'created_at' and 'updated_at' columns. These will automatically 
    be populated with the current time when a record is created or updated.
    """
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


# --- Core Database Models ---
class Leakware(Base):
    """
    Represents a single leak test session, acting as the central point connecting 
    other information.
    """
    __tablename__ = 'leakware'

    leakware_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    mode_of_measurement = Column(String(20), default=None)
    measurement_type = Column(String(20), default=None)
    start_time = Column(DateTime, nullable=False, server_default=func.now())

    data_information = relationship('DataInformation', back_populates='leakware')
    measurements = relationship('Measurements', back_populates='leakware')
    specimens = relationship('Specimens', back_populates='leakware')


class DataInformation(Base):
    """
    Stores metadata associated with a leak test session, including project details,
    element description, and test notes.
    """
    __tablename__ = 'data_information'

    data_information_id = Column(Integer, primary_key=True, autoincrement=True)
    leakware_id = Column(Integer, ForeignKey('leakware.leakware_id'), nullable=False)
    project_number = Column(String(45), default='')
    element = Column(String(45), default='')
    thickness = Column(String(45), default='')
    hole_prepation = Column(String(45), default='')
    coating = Column(String(45), default='')
    direction_of_measurements = Column(String(5), default=None)
    note = Column(String(45), default='')
    date = Column(DateTime, default=None)
    material = Column(String(45), default='')
    die_button = Column(String(45), default='')
    mh_mab = Column(String(45), default='')
    inspector = Column(String(45), default='')
    holesize = Column(String(45), default='')
    material_hardness = Column(String(45), default='')
    installation_force = Column(String(45), default='')
    installation_tooling = Column(String(45), default='')
    active = Column(Boolean, default=False)

    leakware = relationship('Leakware', back_populates='data_information')
    measurements = relationship('Measurements', back_populates='data_information')


class PemSpecificElements(Base):
    """
    Represents specific elements related to PEM testing.

    This class defines the structure of the 'Pem_Specific_Elements' table in the database.
    It includes various attributes related to PEM testing such as project number, inspector,
    date, fastener type, panel information, hole preparation details, installation parameters,
    test directions, notes, and more.

    Attributes:
        pem_specific_id (int): The unique identifier for the PEM specific element.
        leakware_id (int): The ID of the associated leakware.
        project_number (str): The project number related to the testing.
        inspector (str): The name of the inspector.
        date (DateTime): The date of the testing.
        fastener_type (str): The type of fastener used.
        plating_on_fastener (str): The plating on the fastener.
        panel (str): The panel used in the testing.
        plating_on_panel (int): The plating on the panel.
        panel_thickness (str): The thickness of the panel.
        panel_thickness_dia (str): The diameter related to panel thickness.
        hole_diameter (str): The diameter of the hole.
        hole_preparation (str): Details about hole preparation.
        hole_preparation_dia (str): The diameter related to hole preparation.
        panel_hardness (str): The hardness of the panel.
        panel_hardness_type (str): The type of panel hardness.
        install_machine_type (str): The type of installation machine used.
        installation_direction (str): The direction of installation.
        installation_force (str): The force applied during installation.
        installation_anvil (str): The type of installation anvil.
        installation_punch (str): The type of installation punch.
        test_direction_clinch (str): The test direction related to clinching.
        test_direction (str): The general test direction.
        note (str): Additional notes or comments.
        active (bool): Indicates if the record is active or not.
    """
    __tablename__ = 'Pem_Specific_Elements'

    pem_specific_id = Column(Integer, primary_key=True, autoincrement=True)
    leakware_id = Column(Integer, ForeignKey('leakware.leakware_id'), nullable=False)
    project_number = Column(String(45), default='')
    inspector = Column(String(45), default='')
    date = Column(DateTime, default=None)
    fastener_type = Column(String(45), default='')
    plating_on_fastener = Column(String(45), default='')
    panel = Column(String(45), default='')
    plating_on_panel = Column(Integer, default=None)
    panel_thickness = Column(String(45), default='')
    panel_thickness_dia = Column(String(45), default='')
    hole_diameter = Column(String(45), default='')
    hole_preparation = Column(String(45), default='')
    hole_preparation_dia = Column(String(45), default='')
    panel_hardness = Column(String(45), default='')
    panel_hardness_type = Column(String(45), default='')
    install_machine_type = Column(String(45), default='')
    installation_direction = Column(String(45), default='')
    installation_force = Column(String(45), default='')
    installation_anvil = Column(String(45), default='')
    installation_punch = Column(String(45), default='')
    test_direction_clinch = Column(String(45), default='')
    test_direction = Column(String(45), default='')
    note = Column(String, default="")
    active = Column(Boolean, default=True)


class Measurements(Base, TimestampMixin):
    """
    Stores individual measurement readings taken during a leak test session.  
    Includes timestamps and the ability to track multiple readings.
    """
    __tablename__ = 'measurements'

    measerment_Id = Column(Integer, primary_key=True, autoincrement=True)
    leakware_id = Column(Integer, ForeignKey('leakware.leakware_id'), nullable=False)
    data_information_id = Column(Integer, ForeignKey('data_information.data_information_id'),
                                 nullable=True)
    serial_number = Column(Integer, default=None)
    time_in_seconds = Column(Float, default=None)
    value_mbarl_second = Column(Float, default=None)
    max_value = Column(Float, default=None)
    autostop = Column(Integer, default=0)
    panel_no = Column(Integer, nullable=False, default=1)
    location_no = Column(Integer, nullable=False, default=1)
    average_temperature = Column(Float, default=None)
    he_pressure = Column(String(45), default=None)
    he_percentage = Column(String(45), default=None)
    he_massflow_value = Column(String(45), default=None)
    active = Column(Boolean, default=True)

    leakware = relationship('Leakware', back_populates='measurements')
    data_information = relationship('DataInformation', back_populates='measurements')
    specimens = relationship('Specimens', back_populates='measurements')


class Specimens(Base, TimestampMixin):
    """
    Stores X & Y coordinate data likely related to the location of a leak 
    or specific measurement points on a tested element.
    """
    __tablename__ = 'specimens'

    specimen_id = Column(Integer, primary_key=True, autoincrement=True)
    measerment_Id = Column(Integer, ForeignKey('measurements.measerment_Id'), nullable=True)
    x_value = Column(JSON, default=None)
    y_value = Column(JSON, default=None)
    leakware_id = Column(Integer, ForeignKey('leakware.leakware_id'), nullable=False)
    active = Column(Boolean, default=True)

    leakware = relationship('Leakware', back_populates='specimens')
    measurements = relationship('Measurements', back_populates='specimens')

class Devices(Base, TimestampMixin):
    """
    Stores configuration devices, likely related to serial communication with
    external devices.
    """
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True)
    name = Column(String(500), default="None")
    port = Column(String(45), nullable=False)
    baudrate = Column(String(45), default=None)
    bytesize = Column(String(45), default=None)
    parity = Column(String(45), default=None)
    stopbits = Column(String(45), default=None)
    time_out = Column(Float, default=None)
    sccm_value = Column(Float, default=None)
    is_default = Column(Boolean, default=True)
    is_available = Column(Boolean, default=False)

class Report(Base, TimestampMixin):
    """
    Stores Test Images, Type of Medium selected for Test and Notes
    """

    __tablename__ = "report"

    leakware_id = Column(Integer, ForeignKey('leakware.leakware_id'),
                         nullable=False, primary_key=True, autoincrement=False)
    test_medium = Column(String(3), default="He")
    image = Column(String, default="")
    pressure_difference = Column(Integer, default=0)
    rate_unit = Column(String(10), default="")
    note = Column(String, default="")
    graph_type = Column(Integer, default=0)

class MassFlowSensorData(Base, TimestampMixin):
    """
    Stores the values which we received from the mass flow controller
    """

    __tablename__ = "mass_flow_sensor_data"

    device_id = Column(Integer, ForeignKey('devices.device_id'), nullable=True)
    mass_flow_sensor_data_id = Column(Integer, primary_key=True, autoincrement=True)
    psi_v = Column(Float, default=None)
    temp_v = Column(Float, default=None)
    ccm_v = Column(Float, default=None)
    sccm_val = Column(Float, default=None)

class HeliumAnalyzerData(Base, TimestampMixin):
    """
    Stores the values which we received from the helium analyzer
    """

    __tablename__ = "helium_analyzer_data"

    device_id = Column(Integer, ForeignKey('devices.device_id'), nullable=True)
    helium_analyzer_data_id = Column(Integer, primary_key=True, autoincrement=True)
    helium_value = Column(Float, default=None)

class PressureGaugeData(Base, TimestampMixin):
    """
    Stores the values which we received from the Pressure Gauge
    In this pressure stored in bar
    temprature stored in °C
    """

    __tablename__ = "pressure_gauge_data"

    pressure_gauge_data_id = Column(Integer, primary_key=True, autoincrement=True)
    pressure = Column(Float, default=0)
    temperature = Column(Float, default=0)

# Define a function to insert default data
def insert_default_data():
    """
    Insert default data into the database.

    This function inserts default data for devices into the database. Each device
    is represented by its ID, name, port, baudrate, bytesize, parity, stopbits,
    timeout, and other relevant attributes.

    Returns:
        None
    """
    session = Session()

    session.merge(Devices(device_id=1, name='Leak Detector', port="COM11", baudrate=19200,
                          bytesize=8, parity="N", stopbits=1, time_out=0.05,
                          is_available=False, is_default=True))
    session.merge(Devices(device_id=2, name='Mass Flow Controller', port="COM8", baudrate=19200,
                          bytesize=8, parity="N", stopbits=1, time_out=1,
                          sccm_value=71.5, is_available=False, is_default=True))
    session.merge(Devices(device_id=3, name='Helium Analyzer', port="COM6", baudrate=115200,
                          bytesize=8, parity="N", stopbits=1, time_out=1,
                          is_available=False, is_default=True))
    session.merge(Devices(device_id=4, name='Relay Switch', port="COM12", baudrate=9600,
                          bytesize=8, parity="N", stopbits=1, time_out=1,
                          is_available=False, is_default=True))
    session.commit()

    session.close()

Base.metadata.create_all(engine)
insert_default_data()
