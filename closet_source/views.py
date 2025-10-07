from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SourceModel, SourceSerializer
from .serializers import SourceDetailSerializer


class SourceView(APIView):
    def get(self, request):
        sources = SourceModel.objects.all()
        serializer = SourceSerializer(sources, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SourceDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pk = request.data.pop('id')

        i_serializer = SourceDetailSerializer(data=request.data)
        if i_serializer.is_valid():
            source = SourceModel.objects.get(pk=pk)
            for key, value in i_serializer.validated_data.items():
                setattr(source, key, value)
            source.save()
            f_serializer = SourceDetailSerializer(source)
            return Response(f_serializer.data, status=status.HTTP_200_OK)

        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pk = request.data.pop('id')

        i_serializer = SourceDetailSerializer(data=request.data)
        if i_serializer.is_valid():
            source = SourceModel.objects.get(pk=pk)
            for key, value in i_serializer.validated_data.items():
                setattr(source, key, value)
            source.save()
            f_serializer = SourceDetailSerializer(source)
            return Response(f_serializer.data, status=status.HTTP_200_OK)

        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        pk = request.data.pop('id')

        source = SourceModel.objects.get(id=pk)
        source.delete()

        return Response(status=status.HTTP_200_OK)


class SourcePKView(APIView):
    def get(self, request, pk):
        source = SourceModel.objects.filter(id=pk)
        serializer = SourceDetailSerializer(source, many=True)
        return Response(serializer.data[0])

    def post(self, request, pk):

        i_serializer = SourceDetailSerializer(data=request.data)
        if i_serializer.is_valid():
            data = i_serializer.validated_data
            data['id'] = pk

            source = SourceModel.objects.create(**data)
            f_serializer = SourceDetailSerializer(source)

            return Response(f_serializer.data, status=status.HTTP_201_CREATED)
        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        i_serializer = SourceDetailSerializer(data=request.data)
        if i_serializer.is_valid():
            source = SourceModel.objects.get(id=pk)
            for key, value in i_serializer.validated_data.items():
                setattr(source, key, value)
            source.save()
            f_serializer = SourceDetailSerializer(source)
            return Response(f_serializer.data, status=status.HTTP_200_OK)

        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        i_serializer = SourceDetailSerializer(data=request.data)
        if i_serializer.is_valid():
            source = SourceModel.objects.get(id=pk)
            for key, value in i_serializer.validated_data.items():
                setattr(source, key, value)
            source.save()
            f_serializer = SourceDetailSerializer(source)
            return Response(f_serializer.data, status=status.HTTP_200_OK)

        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete(self, request, pk):

        source = SourceModel.objects.get(id=pk)
        source.delete()

        return Response(status=status.HTTP_200_OK)


class BulkSourceView(APIView):
    def get(self, request):
        print("BulkSourceView GET")
        id_list = request.data
        if not id_list:
            sources = SourceModel.objects.all()
            serializer = SourceSerializer(sources, many=True)
        else:
            sources = SourceModel.objects.in_bulk(id_list=id_list, field_name="id")
            serializer = SourceSerializer(list(sources.values()), many=True)
        return Response(serializer.data)

    def post(self, request):
        i_serializer = SourceDetailSerializer(data=request.data, many=True)
        if i_serializer.is_valid():
            data = i_serializer.validated_data
            sources = SourceModel.objects.bulk_create([SourceModel(**d) for d in data])
            f_serializer = SourceDetailSerializer(sources, many=True)
            return Response(f_serializer.data, status=status.HTTP_201_CREATED)
        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        print("BulkSourceView PUT")
        i_serializer = SourceDetailSerializer(data=request.data, many=True)
        if i_serializer.is_valid():
            data = i_serializer.validated_data
            fields = [k for d in data for k in d.keys()]
            print(data)
            sources = SourceModel.objects.bulk_update([SourceModel(**d) for d in data], fields=fields)
            print(sources)
        serializer = S.SourceDetailSerializer(sources, many=True)
        return Response(serializer.data)

    def patch(self, request):
        print("BulkSourceView PATCH")
        request_data = request.data
        sources = SourceModel.objects.bulk_update(
            objs=[SourceModel(**d) for d in request_data],
            fields=list(request_data[0].keys())
        )
        serializer = S.SourceDetailSerializer(sources, many=True)
        return Response(serializer.data)

    def delete(self, request):
        print("BulkSourceView DELETE")
        request_data = request.data
        sources = SourceModel.delete(request_data)
        serializer = S.SourceDetailSerializer(sources, many=True)
        return Response(serializer.data)