from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Dataset
from .serializers import DatasetSerializer
import pandas as pd



class DatasetListAPI(APIView):

    def get(self, request):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatasetComputeView(APIView):

    def post(self, request, name):

        dataset = Dataset.objects.get(name=name)
        column_name = request.data.get('column_name')
        operation = request.data.get('operation')
        
        csv_data = pd.read_csv(dataset.csv_file)
        
        if operation == 'min':
            result = csv_data[column_name].min()
        elif operation == 'max':
            result = csv_data[column_name].max()
        elif operation == 'sum':
            result = csv_data[column_name].sum()
        else:
            return Response({'error': 'Invalid operation'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'result': result})



class DatasetPlotView(APIView):

    def get(self, request, name):

        dataset = Dataset.objects.get(name=name)
        column1 = request.query_params.get('column1')
        column2 = request.query_params.get('column2')

        try:
            csv_data = pd.read_csv(dataset.csv_file)
        except Exception as e:
            return Response({'error': 'Failed to load CSV data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not column1 or not column2:
            return Response({'error': 'Both column1 and column2 are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = csv_data[[column1, column2]][:30].to_dict(orient='records')
        except Exception as e:
            return Response({'error': 'Failed to extract data for plotting.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data)
