import os
import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers


from closet_item.models import ItemModel

from .models import RecommendationModel
from .serializers import RecommendationDetailSerializer


AI_URL = os.getenv("AI_URL")
RECOMMENDATION_URL=f"{AI_URL}/api/ai/recommendations/"

class RecommendationView(APIView):
    def post(self, request):
        query = request.data.pop("query")
        occasions = request.data.pop("occasions")
        item_ids = request.data.pop("items")
        
        selected_item_captions = []
        other_item_captions = []
        all_items = ItemModel.objects.all()
        for d in all_items:
            _id = str(d.id)
            
            if _id in item_ids:
                selected_item_captions.append({"id": _id, "caption": d.caption})
            else:
                other_item_captions.append({"id": _id, "caption": d.caption})
                
        resp = requests.post(
            RECOMMENDATION_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "query": query,
                "occasions": occasions,
                "selected_item_captions": selected_item_captions,
                "other_item_captions": other_item_captions
            })
        ).json()
        
        result = []
        for r in resp:
            items =r["items"]
            comp = r["compatibility"]
            desc = r["description"]
            
            recom = RecommendationModel(compatibility=comp, description=desc)
            recom.save()
            recom.items.set(items)
            
            serializer = RecommendationDetailSerializer(recom, context={"request": request})
            result.append(serializer.data)
            
        return Response(result, status=status.HTTP_200_OK)
