from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from . import models as M
from . import serializers as I
from . import services as V


class RecommendationView(APIView):
    def post(self, request):

        i_serializer = I.RecommendationCreateSerializer(data=request.data, context={'request': request})
        if not i_serializer.is_valid():
            return Response(i_serializer.errors, status.HTTP_400_BAD_REQUEST)

        valid_data = i_serializer.validated_data

        query = valid_data.pop("query")
        occasions = valid_data.pop("occasions")
        item_ids = valid_data.pop("items")

        resp = V.get_recommendations(query, occasions, item_ids)

        result = []
        for r in resp:
            recom = M.RecommendationModel.objects.get(id=r)
            f_serializer = I.RecommendationDetailSerializer(recom, many=False)
            result.append(f_serializer.data)

        # result = M.RecommendationModel.objects.all()
        # f_serializer = I.RecommendationDetailSerializer(result, many=True, context={'request': request})
        # result = f_serializer.data

        return Response(result, status=status.HTTP_200_OK)
