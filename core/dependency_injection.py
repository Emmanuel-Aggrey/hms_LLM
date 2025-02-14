from accounts.services import AccountService
from core.service import CoreService
from doctorsnote.service import DoctorNoteService
from booking.service import BookingService
from actionable_steps.service import ActionableStepsService


class SERVICE_NAMES:
    AccountService = "account_service"
    CoreService = "core_service"
    DoctorNoteService = "doctor_note_service"
    BookingService = "booking_service"
    ActionableStepsService = "actionable_steps_service"


class ServiceLocator:

    service = {}

    account_service: AccountService
    core_service: CoreService
    doctor_booking_service: DoctorNoteService
    booking_service: BookingService
    doctor_note_service: DoctorNoteService
    actionable_steps_service: ActionableStepsService

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services[name]

    def __getitem__(self, name):
        return self.get(name)

    def __getattr__(self, name):
        return self.get(name)


#  register services


service_locator = ServiceLocator()

# Instantiate and register the services

service_locator.register(SERVICE_NAMES.AccountService, AccountService())
service_locator.register(SERVICE_NAMES.CoreService, CoreService())
service_locator.register(SERVICE_NAMES.BookingService, BookingService())
service_locator.register(SERVICE_NAMES.DoctorNoteService, DoctorNoteService())
service_locator.register(
    SERVICE_NAMES.ActionableStepsService, ActionableStepsService())
