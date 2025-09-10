"""
FastAPI endpoints for the TM2 Healthcare Data Ingestion Service.

This module defines the REST API routes for file upload, processing,
and status monitoring.
"""

import time
from datetime import datetime
from typing import Dict, Any
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.logging import get_logger, RequestIDContext, HealthcareOperationContext
from app.core.lifespan import get_mongo_service, get_openmrs_client
from app.services.mongo_service import MongoService
from app.services.openmrs_client import OpenMRSRestClient
from app.services.ingestion_service import TM2IngestionService
from app.models.api_models import (
    ProcessingResult, SystemStatus, ErrorResponse, HealthCheckResponse,
    ProcessingStatus, ServiceStatus, ComponentHealth, ServiceStatistics,
    DatabaseStatistics, OpenMRSStatistics
)

# Initialize router and dependencies
router = APIRouter()
settings = get_settings()
logger = get_logger(__name__)

# Service startup time for uptime calculation
SERVICE_START_TIME = time.time()


def get_ingestion_service(
    mongo_service: MongoService = Depends(get_mongo_service),
    openmrs_client: OpenMRSRestClient = Depends(get_openmrs_client)
) -> TM2IngestionService:
    """
    Dependency to get TM2 ingestion service instance.

    Args:
        mongo_service: MongoDB service dependency
        openmrs_client: OpenMRS client dependency

    Returns:
        TM2IngestionService: Configured ingestion service
    """
    return TM2IngestionService(mongo_service, openmrs_client)


@router.post(
    "/ingest/trigger",
    response_model=ProcessingResult,
    summary="Upload and process TM2 dataset file",
    description="Upload a CSV file containing TM2 dataset records for processing and OpenMRS submission",
    responses={
        200: {"description": "File processed successfully"},
        400: {"description": "Invalid file format or validation errors"},
        422: {"description": "Request validation errors"},
        500: {"description": "Internal server error"}
    }
)
async def trigger_ingestion(
    file: UploadFile = File(..., description="CSV file containing TM2 dataset records"),
    ingestion_service: TM2IngestionService = Depends(get_ingestion_service)
) -> ProcessingResult:
    """
    Upload and process a TM2 dataset file.

    This endpoint accepts CSV files containing TM2 dataset records,
    processes them through the ingestion pipeline, and submits to OpenMRS.

    Args:
        file: CSV file containing TM2 dataset records
        ingestion_service: TM2 ingestion service dependency

    Returns:
        ProcessingResult: Processing results and statistics
    """
    request_id = str(uuid4())

    with HealthcareOperationContext("file_upload"):
        logger.info(
            "File upload initiated",
            filename=file.filename,
            file_size=len(await file.read()),
            request_id=request_id
        )

        # Reset file pointer after reading size
        await file.seek(0)

        try:
            # Validate file type
            if not file.filename.lower().endswith('.csv'):
                raise HTTPException(
                    status_code=400,
                    detail="Only CSV files are supported"
                )

            # Read file content
            file_content = await file.read()

            # Process the file
            result = await ingestion_service.process_tm2_file(
                io.BytesIO(file_content),
                file.filename
            )

            # Convert result to ProcessingResult model
            processing_result = ProcessingResult(
                success=result.get("status") == "completed",
                message=result.get("message", "Processing completed"),
                processing_id=result.get("processing_id"),
                filename=result.get("filename"),
                status=result.get("status"),
                summary=result.get("summary"),
                processing_time_seconds=result.get("processing_time_seconds"),
                emr_output=result.get("emr_output"),
                emr_statistics=result.get("emr_statistics"),
                request_id=request_id
            )

            logger.info(
                "File processing completed successfully",
                processing_id=result.get("processing_id"),
                request_id=request_id
            )

            return processing_result

        except ValueError as e:
            logger.warning(
                "File validation failed",
                filename=file.filename,
                error=str(e),
                request_id=request_id
            )
            raise HTTPException(status_code=400, detail=str(e))

        except Exception as e:
            logger.error(
                "File processing failed",
                filename=file.filename,
                error=str(e),
                request_id=request_id,
                exc_info=True
            )
            raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/status",
    response_model=Dict[str, Any],
    summary="Get system status and statistics",
    description="Retrieve current system status, processing statistics, and service health information"
)
async def get_system_status(
    ingestion_service: TM2IngestionService = Depends(get_ingestion_service)
) -> Dict[str, Any]:
    """
    Get comprehensive system status and processing statistics.

    This endpoint provides real-time information about:
    - Service health and operational status
    - Processing statistics and performance metrics
    - Database and external service connectivity
    - Recent processing activity
    """
    request_id = str(uuid4())

    with RequestIDContext(request_id):
        logger.info("System status requested")

        try:
            # Get processing status from ingestion service
            status_data = await ingestion_service.get_processing_status()

            response = {
                "success": True,
                "message": "System status retrieved successfully",
                "status": status_data,
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat()
            }

            logger.info("System status retrieved successfully")

            return response

        except Exception as e:
            logger.error(
                "Failed to retrieve system status",
                error=str(e),
                exc_info=True
            )

            return {
                "success": False,
                "message": "Failed to retrieve system status",
                "error": str(e),
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat()
            }


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Simple health check for monitoring and load balancer integration"
)
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.

    Returns:
        Dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "tm2-healthcare-service",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get(
    "/data/cleanup-stats",
    response_model=Dict[str, Any],
    summary="Get data cleanup statistics",
    description="Retrieve statistics about data cleaning and quality metrics from recent processing"
)
async def get_data_cleanup_stats(
    ingestion_service: TM2IngestionService = Depends(get_ingestion_service)
) -> Dict[str, Any]:
    """
    Get comprehensive data cleanup and quality statistics.

    This endpoint provides insights into:
    - Data quality scores
    - Field completeness percentages
    - Distribution of severity levels and system types
    - Duplicate and invalid record counts
    - Date range analysis
    """
    request_id = str(uuid4())

    with RequestIDContext(request_id):
        logger.info("Data cleanup statistics requested")

        try:
            # For demo purposes, return mock cleanup statistics
            # In a real implementation, you'd store and retrieve actual cleanup stats
            cleanup_stats = {
                "data_quality_score": 85.5,
                "field_completeness": {
                    "patient_id": 100.0,
                    "tm2_code": 98.5,
                    "condition_name": 97.2,
                    "system_type": 95.8,
                    "severity": 94.1,
                    "diagnosis_date": 96.3,
                    "practitioner_id": 99.2
                },
                "severity_distribution": {
                    "Mild": 35,
                    "Moderate": 45,
                    "Severe": 15,
                    "Critical": 5
                },
                "system_type_distribution": {
                    "Ayurveda": 40,
                    "Siddha": 30,
                    "Unani": 20,
                    "Homeopathy": 10
                },
                "date_range": {
                    "earliest": "2023-01-01T00:00:00",
                    "latest": "2024-09-10T00:00:00"
                },
                "records_processed": 150,
                "duplicates_removed": 5,
                "invalid_records_removed": 3,
                "last_updated": datetime.utcnow().isoformat()
            }

            response = {
                "success": True,
                "message": "Data cleanup statistics retrieved successfully",
                "cleanup_statistics": cleanup_stats,
                "request_id": request_id
            }

            logger.info("Data cleanup statistics retrieved successfully")

            return response

        except Exception as e:
            logger.error(
                "Failed to retrieve data cleanup statistics",
                error=str(e),
                exc_info=True
            )

            return {
                "success": False,
                "message": "Failed to retrieve data cleanup statistics",
                "error": str(e),
                "request_id": request_id
            }


@router.get(
    "/emr/preview",
    response_model=Dict[str, Any],
    summary="Preview EMR conversion output",
    description="Get a preview of how TM2 data would be converted to EMR format"
)
async def preview_emr_conversion(
    ingestion_service: TM2IngestionService = Depends(get_ingestion_service)
) -> Dict[str, Any]:
    """
    Preview EMR conversion for sample data.

    This endpoint shows how TM2 records would be transformed into
    standardized EMR format with patients, conditions, encounters, and observations.
    """
    request_id = str(uuid4())

    with RequestIDContext(request_id):
        logger.info("EMR conversion preview requested")

        try:
            # Sample TM2 data for demonstration
            sample_data = [
                {
                    "patient_id": "PAT001",
                    "tm2_code": "TM2.A01.01",
                    "condition_name": "Chronic Insomnia",
                    "system_type": "Ayurveda",
                    "severity": "Moderate",
                    "diagnosis_date": "2024-01-15",
                    "practitioner_id": "DOC123"
                },
                {
                    "patient_id": "PAT002",
                    "tm2_code": "TM2.B02.03",
                    "condition_name": "Digestive Disorders",
                    "system_type": "Siddha",
                    "severity": "Mild",
                    "diagnosis_date": "2024-02-20",
                    "practitioner_id": "DOC456"
                }
            ]

            # Clean and convert sample data
            cleaned_data, cleanup_stats = ingestion_service._clean_and_summarize_data(sample_data)
            emr_records, emr_stats = ingestion_service._convert_to_emr(cleaned_data)

            # Convert to dictionaries
            emr_output = [record.model_dump() for record in emr_records]

            response = {
                "success": True,
                "message": "EMR conversion preview generated successfully",
                "sample_input": sample_data,
                "cleanup_statistics": cleanup_stats,
                "emr_output": emr_output,
                "emr_statistics": emr_stats,
                "request_id": request_id
            }

            logger.info("EMR conversion preview generated successfully")

            return response

        except Exception as e:
            logger.error(
                "Failed to generate EMR conversion preview",
                error=str(e),
                exc_info=True
            )

            return {
                "success": False,
                "message": "Failed to generate EMR conversion preview",
                "error": str(e),
                "request_id": request_id
            }
