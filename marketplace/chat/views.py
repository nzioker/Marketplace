from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Chat
from .form import ChatMessagesForm

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if item.created_by == request.user:
        return redirect("dashbord:index")
    
    conversations = Chat.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('chat:detail', pk=conversations.first().id)

    if request.method == "POST":
        form = ChatMessagesForm(request.POST)

        if form.is_valid():
            conversation = Chat.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:details', pk=item_pk)
    else:
        form = ChatMessagesForm()

    return render(request, "chat/new.html", {"form":form})

@login_required
def inbox(request):
    conversations = Chat.objects.filter(members__in=[request.user.id])

    return render(request, 'chat/inbox.html', {
        'conversations': conversations
    })


@login_required
def detail(request, pk):
    conversation = Chat.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ChatMessagesForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('chat:detail', pk=pk)
    else:
        form = ChatMessagesForm()

    return render(request, 'chat/detail.html', {
        'conversation': conversation,
        'form': form
    })