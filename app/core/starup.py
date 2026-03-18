# import logging
# from sqlmodel.ext.asyncio.session import AsyncSession
#
# from app.core.config import settings
# from app.database.crud.metadata import SystemMetaCRUD
# from app.core.seed import seed_initial_data, upgrade_initial_data, assert_init_invariants
#
# logger = logging.getLogger(__name__)
#
#
# async def run_initialization(session: AsyncSession) -> None:
#     """
#     Runs on every app startup.
#     Ensures init data is present and up-to-date.
#     Atomic: either fully applies changes or rolls back.
#     """
#     async with session.begin():  # **Label:** One transaction for everything below
#         raw = await SystemMetaCRUD.get_value(session, "init_version")
#
#         if raw is None:
#             logger.warning("Init: init_version missing—database looks new for init data. Running seed.")
#             await seed_initial_data(session)
#             await SystemMetaCRUD.set_value(session, "init_version", str(settings.INIT_DATA_VERSION))
#             await assert_init_invariants(session)
#             return
#
#         try:
#             db_version = int(raw)
#         except ValueError:
#             logger.warning("Init: init_version=%r is not an int—treating as outdated. Running upgrade.", raw)
#             db_version = -1
#
#         if db_version < settings.INIT_DATA_VERSION:
#             logger.warning(
#                 "Init: init_version=%s < %s—database init data is outdated. Running upgrade.",
#                 db_version,
#                 settings.INIT_DATA_VERSION,
#             )
#             await upgrade_initial_data(session, from_version=db_version, to_version=settings.INIT_DATA_VERSION)
#             await SystemMetaCRUD.set_value(session, "init_version", str(settings.INIT_DATA_VERSION))
#             await assert_init_invariants(session)
#             return
#
#         logger.info("Init: init_version=%s is up to date—no action.", db_version)
#         await assert_init_invariants(session)
