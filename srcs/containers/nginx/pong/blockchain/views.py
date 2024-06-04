# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Player
from .utils import generate_wallet, register_player_on_blockchain, update_score_on_blockchain

def register_player(request):
    if request.method == "POST":
        name = request.POST['name']
        eth_address, private_key = generate_wallet()

        tx_hash = register_player_on_blockchain(name, private_key)
        
        player = Player(name=name, eth_address=eth_address, private_key=private_key, score=0)
        player.save()

        return HttpResponse(f"Joueur inscrit avec l'adresse Ethereum : {eth_address}, Transaction Hash: {tx_hash}")

    return render(request, 'register_player.html')

def update_score(request):
    if request.method == "POST":
        eth_address = request.POST['eth_address']
        score = int(request.POST['score'])
        player = Player.objects.get(eth_address=eth_address)
        
        tx_hash = update_score_on_blockchain(eth_address, score, player.private_key)
        player.score = score
        player.save()

        return HttpResponse(f"Score mis à jour pour l'adresse Ethereum : {eth_address}, Transaction Hash: {tx_hash}")

    return render(request, 'update_score.html')
