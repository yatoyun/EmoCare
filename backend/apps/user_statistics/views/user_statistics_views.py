from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.user_statistics.services.user_statistics_services import gather_user_statistics
from apps.user_statistics.models import Statistics

class StatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /statistics
        """
        try:
            stats_response = gather_user_statistics(request.user)
            return Response(stats_response, status=status.HTTP_200_OK)

        except Statistics.DoesNotExist:
            return Response({"error": "cannot find data"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
