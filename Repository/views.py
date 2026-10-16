from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from Repository.models import QuestionDb
from Repository.serializers import QuestionSerializer

# Create your views here.
class QuestionListCreateView(APIView):
    def get(self,request):
        qs=QuestionDb.objects.all()     # Query the QuestionDb model to retrieve all questions
        serializer_instance=QuestionSerializer(qs,many=True) # Serialize the queryset using the QuestionSerializer
        return Response(data=serializer_instance.data)  # Return the serialized data as a response

    def post(self,request):
        form_data=request.data
        serializer_instance=QuestionSerializer(data=form_data)
        if serializer_instance.is_valid():
            actual_data=serializer_instance.validated_data

            # Create a new QuestionDb instance with the form data
            QuestionDb.objects.create(**actual_data)  #kwarg   # Unpack the validated data and create a new QuestionDb instance
            return Response(data={"message":"Question added successfully."})
        else:
            return Response(data={"errors":serializer_instance.errors})

class QuestionRetrieveUpdateDeleteView(APIView):
    def get(self,request,q_id):
        qs=QuestionDb.objects.get(id=q_id)
        serializer_instance=QuestionSerializer(qs)
        return Response(data=serializer_instance.data)
    def put(self,request,q_id):
        form_data=request.data
        serializer_instance=QuestionSerializer(data=form_data)
        if serializer_instance.is_valid():
            actual_data=serializer_instance.validated_data
            QuestionDb.objects.filter(id=q_id).update(**actual_data)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
    def delete(self,request,q_id):
        QuestionDb.objects.filter(id=q_id).delete()
        return Response({"message":"Question deleted successfully"})
        


            