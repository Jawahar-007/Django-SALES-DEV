from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'Burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'