from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from main.util import create_response
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from board.models import Board, Post, Comment
from main.utils.paginator import easy_paginator


class PostListView(TemplateView):
    template_name = 'board/list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        user = request.user
        eng_name = kwargs.get('name')
        category = dict(seminar='세미나', playstorming='플레이스토밍', notice='공지사항', student='재학생 게시판', graduate='졸업생 게시판')
        try:
            board = Board.objects.get(eng_name=eng_name)
        except ObjectDoesNotExist:
            Board(name=category[eng_name], eng_name=eng_name).save()
            return redirect('/main/?warning=잘못된 접근입니다.')

        if board.usable_group and not request.user.groups.filter(
                pk__in=board.usable_group.values_list('pk', flat=True)).exists():
            if not (user.is_superuser or user.is_staff):
                return redirect('/main/?warning=권한이 없습니다.')

        easy_paginator(board.post_set.order_by('-write_date').all(), request.GET.get('page', 1),
                       each_data_count=8, save_to=response)

        response['board'] = board
        response['emphasis_posts'] = board.post_set.filter(emphasis=True).all()

        return render(request, self.template_name, response)


class PostView(TemplateView):
    template_name = 'board/detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        user = request.user

        try:
            board = Board.objects.get(eng_name=kwargs.get('name'))
        except ObjectDoesNotExist:
            return redirect('/main/?warning=잘못된 접근입니다.')

        post = board.post_set.filter(pk=kwargs.get('id'))

        if not post.exists():
            return redirect('/board/%s/?error=존재하지 않는 게시글입니다.' % board.eng_name)
        post = post.first()
        if not request.user == post.writer:
            post.hit += 1
            post.save()

        # 첨부파일 경로 편집
        if post.attachment:
            response['attachment_name'] = post.attachment.name.split("/")[2]

        if board.usable_group and not request.user.groups.filter(
                pk__in=board.usable_group.values_list('pk', flat=True)).exists():

            if not (user.is_superuser or user.is_staff):
                return redirect('/main/?warning=권한이 없습니다.')

        response['post'] = post
        response['comments'] = board.comment_set.filter(post_id=kwargs.get('id')).order_by('-write_date').all()
        response['header_title'] = board.name

        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user

        try:
            board = Board.objects.get(eng_name=kwargs.get('name'))
        except ObjectDoesNotExist:
            return redirect('/main/?warning=잘못된 접근입니다.')

        if board.usable_group and not request.user.groups.filter(
                pk__in=board.usable_group.values_list('pk', flat=True)).exists():

            if not (user.is_superuser or user.is_staff):
                return redirect('/main/?warning=권한이 없습니다.')

        post = board.post_set.filter(pk=kwargs.get('id'))

        if not post.exists():
            return redirect('/board/%s/?error=존재하지 않는 게시글입니다.' % board.eng_name)

        post = post.first()

        if not data.get('content'):
            return redirect('/board/%s/%d?error=입력된 정보가 올바르지 않습니다.' % (board.eng_name, post.pk))

        Comment(
            writer=request.user,
            board=board,
            post=post,
            write_date=timezone.now(),
            content=data.get('content')
        ).save()

        return redirect('/board/%s/%d?success=성공적으로 등록되었습니다.' % (board.eng_name, post.pk))


class PostWriteView(TemplateView):
    template_name = 'board/write.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        user = request.user

        boards = Board.objects.filter(usable_group__in=request.user.groups.all()).all()

        if user.is_superuser or user.is_staff:
            boards = Board.objects.all()

        try:
            board = Board.objects.get(eng_name=request.GET.get('board_name'))
        except ObjectDoesNotExist:
            board = boards.first()

        post = Post.objects.filter(pk=kwargs.get('id'))

        if post.exists():
            response['post'] = post.first()

        response['boards'] = boards
        response['board'] = board
        response['isModify'] = False

        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST

        board_name = data.get('board_name')
        title = data.get('title')
        content = data.get('content')

        if not (board_name and title and content):
            return redirect('/board/write?warning=입력된 정보가 올바르지 않습니다.&board_name=' + board_name)

        try:
            board = Board.objects.get(eng_name=board_name)
        except ObjectDoesNotExist:
            return redirect('/board/write?warning=입력된 정보가 올바르지 않습니다.&board_name=' + board_name)
        Post(
            board=board,
            writer=request.user,
            title=title,
            content=content,
            attachment=request.FILES.get('attachment'),
            thumbnail=request.FILES.get('thumbnail'),
            emphasis=data.get('emphasis', False)
        ).save()

        return redirect('/board/%s/?success=성공적으로 등록되었습니다.' % board_name)


class PostModifyView(TemplateView):
    template_name = 'board/write.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        user = request.user

        try:
            board = Board.objects.get(eng_name=kwargs.get('name'))
        except ObjectDoesNotExist:
            return redirect('/main/?warning=잘못된 접근입니다.')

        if board.usable_group and not request.user.groups.filter(
                pk__in=board.usable_group.values_list('pk', flat=True)).exists():

            if not (user.is_superuser or user.is_staff):
                return redirect('/main/?warning=권한이 없습니다.')

        post = board.post_set.filter(pk=kwargs.get('id'))

        if not post.exists():
            return redirect('/board/%s/?error=존재하지 않는 게시글입니다.' % board.eng_name)
        response['board'] = board
        response['post'] = post.first()
        response['isModify'] = True

        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user

        board_name = data.get('board_name')
        title = data.get('title')
        content = data.get('content')

        if not (board_name and title and content):
            return redirect('/board/write?warning=입력된 정보가 올바르지 않습니다.&board_name=' + board_name)

        try:
            board = Board.objects.get(eng_name=board_name)
        except ObjectDoesNotExist:
            return redirect('/board/write?warning=입력된 정보가 올바르지 않습니다.&board_name=' + board_name)

        if board.usable_group and not request.user.groups.filter(
                pk__in=board.usable_group.values_list('pk', flat=True)).exists():

            if not (user.is_superuser or user.is_staff):
                return redirect('/main/?warning=권한이 없습니다.')

        post = board.post_set.filter(pk=kwargs.get('id'))

        if not post.exists():
            return redirect('/board/%s/?error=존재하지 않는 게시글입니다.' % board.eng_name)

        post = post.first()
        post.title = title
        post.content = content
        if request.FILES.get('attachment'):
            post.attachment = request.FILES.get('attachment')
        if request.FILES.get('thumbnail'):
            post.thumbnail = request.FILES.get('thumbnail')
        post.emphasis = data.get('emphasis', False)

        post.save()

        return redirect('/board/%s/%d?success=수정되었습니다.' % (board_name, post.pk))


class PostDeleteView(TemplateView):
    template_name = 'board/list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        user = request.user

        try:
            board = Board.objects.get(eng_name=kwargs.get('name'))
        except ObjectDoesNotExist:
            return redirect('/main/?warning=잘못된 접근입니다.')

        if board.usable_group and not request.user.groups.filter(
                pk__in=board.usable_group.values_list('pk', flat=True)).exists():

            if not (user.is_superuser or user.is_staff):
                return redirect('/main/?warning=권한이 없습니다.')

        post = board.post_set.filter(pk=kwargs.get('id'))

        if not post.exists():
            return redirect('/board/%s/?error=존재하지 않는 게시글입니다.' % board.eng_name)

        post.first().delete()

        return redirect('/board/%s/?success=삭제되었습니다.' % kwargs.get('name'))
