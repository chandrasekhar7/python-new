"""
repository.py: Data Access Layer for Leakware

This file implements the Repository pattern, providing a centralized interface for interacting with
the Leakware database. It encapsulates various database operations, such as creating leakware
sessions,inserting measurements, retrieving data, updating device information, and committing
changes.

Key Class:
- Repository:
  - __init__(self, session): Initializes the Repository with a SQLAlchemy session object.
  - create_leakware(self, time, mode_of_measurement, measurement_type): Creates a new Leakware entry.
  - insert_data_information(self, data_information): Adds a DataInformation record.
  - insert_penn_specific_elements(self, data_penn_specific): Adds a PemSpecificElements record.
  - insert_measurement(self, measurements): Adds a Measurements record.
  - insert_specimens(self, specimens): Adds a Specimens record.
  - save_devices(self, devices): Saves the session devices.
  - get_all_specimens(self, leakware_id): Retrieves all Specimen records for a leak test.
  - get_all_data_information(self, leakware_id, data_information_id): Retrieves a specific DataInformation record.
  - get_all_measurements_data(self, leakware_id): Retrieves all measurement data for a leak test session.
  - update_measurement_by_id(self, measurement_id, column_name, column_value): Updates a measurement record by ID.
- get_panel_and_location_number(self, leakware_id): Retrieves the panel and location number for a leak test session.
- get_specification(self, leakware_id, mode_of_measurement): Retrieves the specification data for a leak test session.
- save_report_data(self, report): Saves the report data for a leak test session.
- delete_last_measurement(self, leakware_id): Deletes the last measurement entry for a leak test session.
- get_device_info_by(self, name): Retrieves device information by name.
- commit(self): Commits the session changes to the database.
- close_session(self): Closes the database session.
- update_device_info(self): Updates the device information in the database.
- get_device_serial_info_by(self, name): Retrieves serial device information by name.
- create_mass_flow_sensor_data(self, mass_flow_sensor_data): Creates a MassFlowSensorData record.
- create_helium_analyzer_data(self, helium_analyzer_data): Creates a HeliumAnalyzerData record.
- create_pressure_gauge_data(self, pressure_gauge_data): Creates a PressureGaugeData record.
- get_sensor_data(self): Retrieves sensor data from the database.

Dependencies:
- logging
- sqlalchemy.orm
- sqlalchemy
- sqlalchemy.exc
- db_model

Usage:
This module is typically imported and an instance of the Repository class is created, passing in
a SQLAlchemy session object. The Repository instance provides a centralized interface for interacting
with the database, abstracting away the underlying database operations and promoting code organization
and maintainability.
"""
# -------------------------------
# repository.py: Data Access Layer for Leakware
# -------------------------------
import logging

# This file implements the Repository pattern, providing a centralized interface for
# interacting with the Leakware database. It encapsulates database operations, promoting
# separation of concerns and making the rest of the application code cleaner.

from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy import select, and_, desc
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from db_model import Leakware, DataInformation, Measurements, Specimens, Devices, PemSpecificElements, Report
from db_model import PressureGaugeData, MassFlowSensorData, HeliumAnalyzerData, engine

# Create a session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

class Repository:
    # Acts as the primary interaction point with the Leakware database.

    def __init__(self, session: Session):
        """
        Initializes the Repository with a SQLAlchemy session object. This session 
        manages the connection and transactions with the database.

        Args:
            session (Session): A SQLAlchemy session object.

        self.session: Session = session
        """
        self.session = Session()

    # Creates a new Leakware entry representing a test session.
    def create_leakware(self, time, mode_of_measurement, measurement_type):
        '''
        Create the leakware id
        '''
        leakware = Leakware(start_time=time, mode_of_measurement=mode_of_measurement, measurement_type=measurement_type)
        self.session.add(leakware)
        self.session.commit()
        return leakware

    # Adds a DataInformation record (tied to a leak test session).
    def insert_data_information(self, data_information: DataInformation):
        '''
        Insert the profil mode element specification information.
        '''
        self.session.add(data_information)
        self.session.commit()
        return data_information

    def insert_penn_specific_elements(self, data_penn_specific: PemSpecificElements):
        '''
        insert pem mode specific elements
        '''
        self.session.add(data_penn_specific)
        self.session.commit()
        return data_penn_specific

    # Adds a Measurements record (tied to a leak test session).
    def insert_measurement(self, measurements: Measurements):
        '''
        Insert measurement data
        '''
        self.session.add(measurements)
        self.session.commit()
        return measurements

    # Adds a specimen record (tied to a leak test session)
    def insert_specimens(self, specimens: Specimens):
        '''
        Insert the specimen data using the session
        '''
        self.session.add(specimens)
        self.session.commit()
        return specimens

    # Saves the session devices.
    def save_devices(self, devices: Devices):
        '''
        save device information by using Devices object
        '''
        self.session.add(devices)
        self.session.commit()
        return devices

    # Retrieves all Specimen records associated with a leak test.
    def get_all_specimens(self, leakware_id):
        '''
        get all the specimens
        '''
        try:
            stmt = select(Specimens).filter_by(leakware_id=leakware_id, active=True)
            specimens = self.session.scalars(stmt).all()
            return specimens
        except Exception as e:
            # Log the error for debugging purposes
            logging.error("Error occurred while retrieving specimens: %s", str(e))

            # Rollback the transaction if an error occurs
            self.session.rollback()

            # Re-raise the exception for proper error handling
            raise

    # Retrieves a specific DataInformation record using filters.
    def get_all_data_information(self, leakware_id, data_information_id) -> DataInformation:
        '''get all data information'''
        stmt =\
            select(DataInformation).filter_by(
                leakware_id=leakware_id
            ).where(
                and_(DataInformation.data_information_id == data_information_id)
            )
        data_information = self.session.scalar(stmt)
        return data_information

    # Retrieves all measurement data for a leak test session.
    def get_all_measurements_data(self, leakware_id):
        '''
        Get all the measurement data by using the leakware id
        '''
        stmt = select(Measurements).filter_by(leakware_id=leakware_id, active=True)
        measurements_data = self.session.scalars(stmt).all()
        return measurements_data

    # update measurement by id
    def update_measurement_by_id(self, measurement_id, column_name, column_value):
        '''
        update the measurement data by using the measurement id
        '''
        try:
            measurement = self.session.query(Measurements).filter_by(measerment_Id=measurement_id).first()
            if measurement:
                setattr(measurement, column_name, column_value)
                #self.session.commit()
                return True
            else:
                print(f"Measurement with ID {measurement_id} not found.")
                logging.error("Measurement with ID %s not found in update_measurement_by_id in repository", measurement_id)
                return False
        except Exception as e:
            print("An error occurred while updating measurement:", e)
            logging.error("An error occurred while updating measurement in update_measurement_by_id: %s", e)
            return False

    # Retrieves all measurement data for a leak test session.
    def get_panel_and_location_number(self, leakware_id):
        '''
        Get panel and location number
        '''
        try:
            stmt = select(Measurements).filter_by(
                leakware_id=leakware_id, active=True
            ).order_by(
                desc(Measurements.measerment_Id)
            )
            measurement = self.session.execute(stmt).scalar()
            if measurement:
                return measurement.panel_no, measurement.location_no + 1
            else:
                return 1, 1  # Return default values if no measurements are found
        except NoResultFound:
            print("No results found")
            return 1, 1
        except SQLAlchemyError as e:  # Catching a more specific database-related exception
            print(f"An SQL Error occurred in get_panel_and_location_number: {e}")
            self.session.rollback()
            return 1, 1

    def get_specification(self, leakware_id, mode_of_measurement):
        '''
        Get specification details based on leakware id and mode of measurements.
        '''
        if mode_of_measurement == "PEM":
            stmt = select(PemSpecificElements).filter_by(
                leakware_id=leakware_id
            ).order_by(
                desc(PemSpecificElements.pem_specific_id)
            )
        else:
            stmt = select(DataInformation).filter_by(
                leakware_id=leakware_id
            ).order_by(
                desc(DataInformation.data_information_id)
            )
        specification = self.session.execute(stmt).scalar()
        return specification

    def save_report_data(self, report: Report) -> Report:
        '''
        save the report data
        '''
        try:
            # Merge the report data into the session
            self.session.merge(report)
            self.session.commit()
            return report
        except Exception as e:
            self.session.rollback()
            logging.error("Error occurred while saving report data: %s", str(e))
            raise


    def delete_last_measurement(self, leakware_id):
        '''
        Delete the last measurement
        '''
        try:
            stmt = select(Measurements).filter_by(
                leakware_id=leakware_id,
                active=True
            ).order_by(
                desc(Measurements.measerment_Id)
            )
            measurement = self.session.execute(stmt).scalar()
            if measurement:
                setattr(measurement, "active", False)
                specimen_select = select(Specimens).filter_by(
                    leakware_id=leakware_id,
                    measerment_Id=measurement.measerment_Id,
                    active=True
                )
                specimen = self.session.execute(specimen_select).scalar()
                if specimen:
                    setattr(specimen, "active", False)
                self.session.commit()
            else:
                print("Measurement not found.")
        except SQLAlchemyError as e:
            # Handle the exception here
            print("An error occurred in delete_last_measurement. Rollback session issued:", e)
            # Optionally, rollback the session if necessary
            self.session.rollback()

    def get_device_info_by(self, name):
        '''
        Get the device information by using the name
        '''
        stmt = select(Devices).filter_by(name=name)
        result = self.session.execute(stmt).scalar()
        return result

    def commit(self):
        '''
        commit the changes based on the session
        '''
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def close_session(self):
        '''
        close the session
        '''
        self.session.close()

    def update_device_info(self):
        '''
        Update the device information into db
        '''
        self.session.commit()

    def get_device_serial_info_by(self, name):
        '''
        get the device information by using name
        '''
        stmt = select(Devices).filter_by(name=name)
        device = self.session.execute(stmt).scalar()
        return {
            'baudrate': device.baudrate,
            'bytesize': device.bytesize,
            'parity': device.parity,
            'stopbits': device.stopbits,
            'timeout': device.time_out
        }

    def create_mass_flow_sensor_data(self, mass_flow_sensor_data: MassFlowSensorData):
        '''
        Create the massflow sensor data
        '''
        self.session.add(mass_flow_sensor_data)
        self.session.commit()
        return mass_flow_sensor_data

    def create_helium_analyzer_data(self, helium_analyzer_data: HeliumAnalyzerData):
        '''
        is using for create the helium analyzer data
        '''
        self.session.add(helium_analyzer_data)
        self.session.commit()
        return helium_analyzer_data

    def create_pressure_gauge_data(self, pressure_gauge_data: PressureGaugeData):
        '''
        Method is used to create the pressure gauge data.
        '''
        self.session.add(pressure_gauge_data)
        self.session.commit()
        return pressure_gauge_data

    def get_sensor_data(self):
        '''
        This method is using for fetching the sensor data from three different tables.
        '''
        stmt = select(PressureGaugeData).order_by(desc(PressureGaugeData.pressure_gauge_data_id))
        stmt2 = select(HeliumAnalyzerData).order_by(desc(HeliumAnalyzerData.helium_analyzer_data_id))
        stmt3 = select(MassFlowSensorData).order_by(desc(MassFlowSensorData.mass_flow_sensor_data_id))
        # Initialize default values
        temperature = 0
        pressure = 0
        helium = 0
        sccm_value = 0
        try:
            # Executing query
            pressure_gauge = self.session.execute(stmt).scalar()
            helium_analyzer = self.session.execute(stmt2).scalar()
            mass_flow_controller = self.session.execute(stmt3).scalar()
            # Accessing data if available
            if pressure_gauge:
                temperature = pressure_gauge.temperature
                pressure = pressure_gauge.pressure
            if helium_analyzer:
                helium = helium_analyzer.helium_value
            if mass_flow_controller:
                sccm_value = mass_flow_controller.sccm_val
        except NoResultFound:
            # Handle the case when there is no data found
            print("No data found in the tables")
        return {
            'temperature': temperature,
            'pressure': pressure,
            'helium': helium,
            'sccm_value': sccm_value
        }
