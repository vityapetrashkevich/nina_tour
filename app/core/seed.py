import logging
from sqlmodel.ext.asyncio.session import AsyncSession
from packaging.version import parse as parse_version

from app.database.crud.admin import AdminCRUD
from app.database.crud.metadata import SystemMetaCRUD
from app.core.config import settings
from app.core.utils import read_yaml_async
from app.schemas.admins import AdminRegisterRequest, AdminRegisterResponse

logger = logging.getLogger(__name__)


# async def seed_initial_data(session: AsyncSession, data: dict) -> AdminRegisterResponse:
#     try:
#         admin = AdminRegisterRequest(**data.get('admin')[0])
#         admin, password = await AdminCRUD.create(session, admin)
#         return AdminRegisterResponse(
#             id=admin.id,
#             email=admin.email,
#             generated_password=password,
#         )
#     except (KeyError, IndexError):
#         logger.exception('Error while creating admin. Validate init_data.yaml.')
#         raise KeyError('Error while creating admin. Validate init_data.yaml.')
#
#
# async def update_metadata(session: AsyncSession, meta: dict) -> bool:
#     try:
#         for key, value in meta.items():
#             await SystemMetaCRUD.set_value(session, key=key, value=value)
#         return True
#     except KeyError:
#         logger.error("Some metadata does not valid or loss, cannot run application. "
#                      "Please update your repository and try again.")
#         raise KeyError(
#             "Some metadata does not valid or loss, cannot run application. Please update your repository"
#             " and try again.")
#
#
# async def run_initialization(session: AsyncSession) -> None:
#     """
#     Runs on every app startup.
#     Ensures init data is present and up-to-date.
#     Atomic: either fully applies changes or rolls back.
#     """
#     async with (session.begin()):  # **Label:** One transaction for everything below
#         meta, init_data = await read_yaml_async(settings.INIT_DATA_FILE)
#         meta = meta.get('Metadata')
#         if not meta:
#             logger.error("No metadata found, cannot run initialization. Please update your repository and try again.")
#             raise ValueError("No metadata found, cannot run initialization. "
#                              "Please update your repository and try again.")
#         current_meta_ver = await SystemMetaCRUD.get_value(session, "metadata_version")
#         if current_meta_ver is None:
#             logger.warning("Init: init_version missing—database looks new for init data. Running seed.")
#             await update_metadata(session, meta)
#             await seed_initial_data(session, init_data)
#         else:
#             if parse_version(meta.get('metadata_version')) > parse_version(current_meta_ver):
#                 await update_metadata(session, meta)
#             current_init_ver = await SystemMetaCRUD.get_value(session, "init_data_version")
#             if parse_version(meta.get('init_data_version')) > parse_version(current_init_ver):
#                 pass
#         logger.info("Init: metadata_version=%s is up to date—no action.", meta.get('metadata_version'))
#         logger.info("Init: init_data_version=%s is up to date—no action.", meta.get('init_data_version'))

async def seed_initial_data(session: AsyncSession, init_data: dict):
    try:
        admins = init_data.get("admin")
        print(admins)
        if not admins:
            raise KeyError("Missing 'admin' section in init_data.yaml")

        admin_payload = AdminRegisterRequest(**admins[0])
        admin, password = await AdminCRUD.create(session, admin_payload, init=True)
        print(admin)
        print(password)
        return admin_payload.email, password

    except (KeyError, IndexError, TypeError) as e:
        logger.exception("Invalid admin structure in init_data.yaml: %s", e)
        raise KeyError("Invalid admin structure in init_data.yaml: %s", e)


async def update_metadata(session: AsyncSession, meta: dict) -> None:
    if not isinstance(meta, dict):
        logger.error("Metadata must be a dict")
        raise ValueError("Metadata must be a dict")

    for key, value in meta.items():
        await SystemMetaCRUD.set_value(session, key=key, value=value)


async def run_initialization(session: AsyncSession) -> None:
    async with session.begin():
        meta, init_data = await read_yaml_async(settings.INIT_DATA_FILE)
        meta = meta.get("Metadata")
        if not meta:
            logger.error("Missing 'Metadata' section in init_data.yaml")
            raise ValueError("Missing 'Metadata' section in init_data.yaml")

        new_meta_ver = meta.get("metadata_version")
        new_init_ver = meta.get("init_data_version")
        current_meta_ver = await SystemMetaCRUD.get_value(session, "metadata_version")
        current_init_ver = await SystemMetaCRUD.get_value(session, "init_data_version")
        # Fresh DB
        if current_meta_ver is None:
            logger.warning("Database appears new. Seeding initial data.")
            await update_metadata(session, meta)
            admin =await seed_initial_data(session, init_data)
            print(admin)
        else:
            # Metadata update
            if parse_version(new_meta_ver) > parse_version(current_meta_ver):
                logger.info("Updating metadata to version %s", new_meta_ver)
                await update_metadata(session, meta)
            # Init data update
            # if parse_version(new_init_ver) > parse_version(current_init_ver):
            #     logger.info("Updating init data to version %s", new_init_ver)
            #     await seed_initial_data(session, init_data)
            #     await SystemMetaCRUD.set_value(session, "init_data_version", new_init_ver)

        logger.info("Initialization complete. Everything up to date.")
        print('Initialization complete. Everything up to date.')
