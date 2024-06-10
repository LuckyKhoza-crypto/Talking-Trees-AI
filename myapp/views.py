from dotenv import load_dotenv
import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponse
from .models import trees_Database as Tree
from .forms import TreeSearchForm, CommentForm
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
# this is the filter class that will be used to filter the trees in the database for the advanced search
from .filters import TreeFilter
from rest_framework import generics, parsers
from rest_framework.response import Response
from .serializer import TreeResourceSerializer
import pandas as pd  # import the pandas module which is used to read the csv file

from .models import trees_Database as Tree
from .models import TreeResource, Comment

# Chatbot libraries
# from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chroma import Chroma
from langchain_openai import ChatOpenAI
import datetime
from langchain.chains import RetrievalQA
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter

import os
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.


def searchBar(request):
    # loads the form for the search bar, it is avaliable globally through TEMPLATES in settings.py
    return {'myFilter': TreeFilter()}

# this function prints the login message to the user


def login_message(request):
    return messages.info(
        request, 'You are not logged in. Please login with your Whitman College credentials.')


def home(request):
    myFilter = TreeFilter()
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        # return user to login page if not authenticated
        return redirect('/accounts/login', context={login_message(request)})


def advancedSearch(request):
    message = None
    if not request.user.is_authenticated:
        return redirect('/accounts/login', context={login_message(request)})

    if request.method == 'GET':
        searchResult = Tree.objects.all()
        totalTrees = searchResult.count()

        # using the filter we created to filter the trees in the database
        myFilter = TreeFilter(request.GET, queryset=searchResult)

        searchResult = myFilter.qs  # the trees that match the filter
        # the number of trees that match the filter
        searchResultCount = searchResult.count()

        if searchResultCount < totalTrees:  # if the trees returned are less than the total trees in the database, then there was a query passed on the filter
            if searchResult:  # if there are trees that match the filter
                myFilter = TreeFilter()  # reset the filter
                context = {'searchResult': searchResult,
                           'myFilter': myFilter, 'message': message}
                # render the advancedSearchResult.html page with the trees that match the filter
                return render(request, "advancedSearchResult.html", context)


def randomSearchResult(request):
    myFilter = TreeFilter()
    message = None
    if not request.user.is_authenticated:
        return redirect('/accounts/login', context={login_message(request)})

    if request.method == 'GET':
        searchResult = Tree.objects.all()
        randomTree = searchResult.order_by('?').first()
        searchResult = randomTree
        context = {'searchResult': searchResult, 'message': message}
        return render(request, "randomSearchResult.html", context)


def post_comment(request, tree_id):

    comments = Comment.objects.filter(
        tree_id__tree_id=tree_id, moderated=True).order_by('-created')

    tree = get_object_or_404(Tree, tree_id=tree_id)

    if request.method == 'GET':
        form = CommentForm()
        return render(request, 'comments.html', {'form': form, 'comments': comments, 'tree': tree})

    else:
        print("it's a post request")
        form = CommentForm(request.POST)
        comment = None
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tree_id = tree
            comment.save()

            return redirect('post_comment', tree_id=tree_id)


class import_Data(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser]
    serializer_class = TreeResourceSerializer

    def post(self, request, *args, **kwargs):

        file = request.FILES['excel']

        if 'excel' not in request.FILES:
            return JsonResponse({'error': 'No excel file provided.'}, status=400)

        # read the excel file using pandas
        df = pd.read_excel(file, engine='openpyxl')

        df.rename(columns={
            'OBJECTID': 'id',
            'Lat': 'latitude',
            'Long': 'longitude',
            'Alt_ft': 'altitude_ft',
            'Tree_ID': 'tree_id',
            'Zone': 'zone',
            'Group_': 'group_name',
            'Leaf_Fall': 'leaf_fall',
            'Common_Name': 'common_name',
            'Genus': 'genus',
            'Species_Name': 'species_name',
            'Family': 'family_name',
            'CBH': 'cbh',
            'DBH': 'dbh',
            'Tree_Height_ft': 'tree_height_ft',
            'Canopy_Radius_ft': 'canopy_radius_ft'
        }, inplace=True)

        for index, row in df.iterrows():
            defaults = row.to_dict()
            tree_id = defaults.pop('tree_id', None)

            Tree.objects.update_or_create(
                tree_id=tree_id, defaults=defaults)
        result = Tree.objects.all()

        return Response({"status": "success"})

    def get(self, request, *args, **kwargs):
        pass
        return Response({"status": "success"})


CHATBOT_CONTEXT_STRING = "The dataset you have is a collection of all \
the trees on Whitman College campus in Walla Walla, Washington. Each tree has a unique ID number and associated data with it, \
such as species, coordinates, height, etc. I want you to absorb all the information in \
the dataset so that you can answer specific questions about trees. Tree ID's are represented by one letter followed by a few digits. \
For example, C60 is a Tree ID. Whenever you are asked about a certain tree, provide its Tree ID that is located in that row of the dataset. \
The tree data is organized by columns. Waypoint is a number representing the tree's location. Alt_ft represents the tree's altitude, which is different than its height. \
Trees are given a common name, denoted by the Common Name column. There are also columns for Genus and Species Name. Trees belong to different families, such as Fabaceae and Pinaceae. \
You need to absorb all this information and be able to tell me ALL the trees of a particular genus, family name, or species. Whenever I'm asking for a particular tree or trees, provide their tree IDs as well.\
Keep in mind there are more than 2000 rows in the dataset so you need to process a lot of information. The height of every tree can be found under the height column."

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def display_chatbot_response(request):
    if request.method == 'POST':
        # Get the user input from the POST request
        user_input = request.POST.get('user_input', '')
        # Pass the user input to the chatbot function
        chatbot_response = generate_chatbot_response(
            CHATBOT_CONTEXT_STRING + user_input)
        print(chatbot_response)
        return HttpResponse(chatbot_response)

    return render(request, 'chat.html')


def chat_view(request):
    return render(request, "chatinplace.html")


qa_chain = None
vectordb = None


def initialize_openai():
    global qa_chain, vectordb
    print("Initializing OpenAI...")
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Load PDF dataset
    # loader = PyPDFLoader("TreeData.pdf")

    # Load Excel dataset instead
    # loader = UnstructuredExcelLoader("TreeData.xlsx")

    loader = CSVLoader("Trees.csv")
    data = loader.load()
    # pages = loader.load()

    # Split data into chunks
    # r_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=450,
    #     chunk_overlap=0,
    #     separators=["\n\n", "\n", " ", ""]
    # )
    # docs = r_splitter.split_documents(pages)
    # print (f'{docs=}')

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    split_data = text_splitter.split_documents(data)

    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma.from_documents(
        documents=split_data,
        embedding=embedding
    )

    # Initialize vector database
    # vectordb = Chroma.from_documents(
    #     documents=docs,
    #     embedding=embedding
    #  )

    current_date = datetime.datetime.now().date()
    if current_date < datetime.date(2023, 9, 2):
        llm_name = "gpt-3.5-turbo-0301"
    else:
        llm_name = "gpt-3.5-turbo"

        # Initialize chatbot model
    llm = ChatOpenAI(model_name=llm_name, temperature=0,
                     openai_api_key=OPENAI_API_KEY)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever()
    )

    print(
        qa_chain({"query": "Tell me about the trees on the Whitman College campus."}))

    print("...finished initializing OpenAI")


initialize_openai()


def generate_chatbot_response(user_input):
    global qa_chain, vectordb
    # Use LLM model to generate a response

    sim_search = vectordb.similarity_search(user_input, 30)
    chatbot_response = qa_chain({"query": user_input + str(sim_search)})
    return chatbot_response["result"]
