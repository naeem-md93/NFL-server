from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import (
    serializers as I,
    models as M,
    services as V
)


class ClosetImageView(APIView):
    def get(self, request):

        _id = request.GET.get('id', None)

        if _id is None:
            images = M.ImageModel.objects.all()
            resp_data = I.ImageListSerializer(images, many=True, context={'request': request}).data
            return Response(resp_data, status=status.HTTP_200_OK)

        image = M.ImageModel.objects.get(id=_id)
        resp_data = I.ImageDetailSerializer(image, context={'request': request}).data
        return Response(resp_data, status=status.HTTP_200_OK)

    def post(self, request):
        i_serializer = I.ImageCreateSerializer(data=request.data, context={'request': request})
        if i_serializer.is_valid():
            valid_data = i_serializer.validated_data
            file = valid_data.pop("file", None)
            image = V.process_and_store_image(file)
            f_serializer = I.ImageDetailSerializer(image, context={'request': request})
            return Response(f_serializer.data, status=status.HTTP_200_OK)
        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        _id = request.data.pop("id")
        image = M.ImageModel.objects.get(id=_id)
        image.delete()
        return Response(data={"Deleted Successfully"}, status=status.HTTP_200_OK)


class ClosetItemView(APIView):
    def get(self, request):

        _id = request.GET.dict().pop('id', None)

        if _id is None:
            sources = M.ItemModel.objects.all()
            serializer = I.ItemListSerializer(sources, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)


        item = M.ItemModel.objects.get(id=_id)
        resp_data = I.ItemDetailSerializer(item, context={"request": request})

        return Response(resp_data, status=status.HTTP_200_OK)
