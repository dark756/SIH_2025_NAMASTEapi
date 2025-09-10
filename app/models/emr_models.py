"""
Electronic Medical Record (EMR) models for TM2 healthcare data.

This module defines models for converting TM2 data into standardized
EMR format compatible with systems like OpenMRS and FHIR.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class EMRPatient(BaseModel):
    """
    EMR Patient record model.
    """
    model_config = ConfigDict(use_enum_values=True)

    patient_id: str = Field(
        ...,
        description="Unique patient identifier in EMR system"
    )

    given_name: Optional[str] = Field(
        default=None,
        description="Patient's given name"
    )

    family_name: Optional[str] = Field(
        default=None,
        description="Patient's family name"
    )

    gender: Optional[str] = Field(
        default=None,
        description="Patient gender"
    )

    birth_date: Optional[datetime] = Field(
        default=None,
        description="Patient birth date"
    )

    address: Optional[str] = Field(
        default=None,
        description="Patient address"
    )

    phone_number: Optional[str] = Field(
        default=None,
        description="Patient phone number"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )


class EMRCondition(BaseModel):
    """
    EMR Condition/Diagnosis record model.
    """
    model_config = ConfigDict(use_enum_values=True)

    condition_id: str = Field(
        ...,
        description="Unique condition identifier"
    )

    patient_id: str = Field(
        ...,
        description="Associated patient identifier"
    )

    condition_name: str = Field(
        ...,
        description="Name of the medical condition"
    )

    icd_code: Optional[str] = Field(
        default=None,
        description="ICD code for the condition"
    )

    tm2_code: str = Field(
        ...,
        description="Original TM2 code"
    )

    system_type: str = Field(
        ...,
        description="Traditional medicine system"
    )

    severity: str = Field(
        ...,
        description="Condition severity"
    )

    diagnosis_date: datetime = Field(
        ...,
        description="Date of diagnosis"
    )

    practitioner_id: str = Field(
        ...,
        description="Healthcare practitioner identifier"
    )

    status: str = Field(
        default="active",
        description="Condition status"
    )

    notes: Optional[str] = Field(
        default=None,
        description="Additional clinical notes"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )


class EMREncounter(BaseModel):
    """
    EMR Encounter record model.
    """
    model_config = ConfigDict(use_enum_values=True)

    encounter_id: str = Field(
        ...,
        description="Unique encounter identifier"
    )

    patient_id: str = Field(
        ...,
        description="Associated patient identifier"
    )

    encounter_type: str = Field(
        default="traditional_medicine_consultation",
        description="Type of encounter"
    )

    encounter_date: datetime = Field(
        ...,
        description="Date and time of encounter"
    )

    practitioner_id: str = Field(
        ...,
        description="Healthcare practitioner identifier"
    )

    location: Optional[str] = Field(
        default=None,
        description="Encounter location"
    )

    conditions: List[str] = Field(
        default_factory=list,
        description="List of condition IDs addressed in this encounter"
    )

    observations: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Clinical observations from the encounter"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )


class EMRObservation(BaseModel):
    """
    EMR Observation/Vital record model.
    """
    model_config = ConfigDict(use_enum_values=True)

    observation_id: str = Field(
        ...,
        description="Unique observation identifier"
    )

    patient_id: str = Field(
        ...,
        description="Associated patient identifier"
    )

    encounter_id: Optional[str] = Field(
        default=None,
        description="Associated encounter identifier"
    )

    concept: str = Field(
        ...,
        description="Observation concept/type"
    )

    value: Any = Field(
        ...,
        description="Observation value"
    )

    units: Optional[str] = Field(
        default=None,
        description="Units for numeric values"
    )

    observation_date: datetime = Field(
        ...,
        description="Date and time of observation"
    )

    practitioner_id: str = Field(
        ...,
        description="Healthcare practitioner identifier"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )


class EMRRecord(BaseModel):
    """
    Complete EMR record combining patient, conditions, encounters, and observations.
    """
    model_config = ConfigDict(use_enum_values=True)

    patient: EMRPatient = Field(
        ...,
        description="Patient demographic information"
    )

    conditions: List[EMRCondition] = Field(
        default_factory=list,
        description="List of patient conditions/diagnoses"
    )

    encounters: List[EMREncounter] = Field(
        default_factory=list,
        description="List of patient encounters"
    )

    observations: List[EMRObservation] = Field(
        default_factory=list,
        description="List of clinical observations"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the EMR record"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="EMR record creation timestamp"
    )


class EMRStatistics(BaseModel):
    """
    Statistics for EMR conversion process.
    """
    model_config = ConfigDict(use_enum_values=True)

    total_records_processed: int = Field(
        default=0,
        description="Total TM2 records processed for EMR conversion"
    )

    patients_created: int = Field(
        default=0,
        description="Number of unique patients created in EMR"
    )

    conditions_created: int = Field(
        default=0,
        description="Number of conditions created in EMR"
    )

    encounters_created: int = Field(
        default=0,
        description="Number of encounters created in EMR"
    )

    observations_created: int = Field(
        default=0,
        description="Number of observations created in EMR"
    )

    conversion_errors: int = Field(
        default=0,
        description="Number of conversion errors"
    )

    data_quality_score: float = Field(
        default=0.0,
        description="Overall data quality score (0-100)"
    )

    processing_time_seconds: Optional[float] = Field(
        default=None,
        description="Time taken for EMR conversion"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Statistics generation timestamp"
    )
