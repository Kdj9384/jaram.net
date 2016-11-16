from board.models import Post, Board
from main.models import Member, Grade, Notice
from schedule.models import Event
from django.utils.datetime_safe import datetime, date
from datetime import timedelta
import calendar
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from main.util import create_response


class IntroView(TemplateView):
    template_name = 'intro.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        
        today = date.today()
        year = today.year
        month = today.month
        calendar.setfirstweekday(calendar.SUNDAY)
        
        event_dates = []
        events = Event.objects.filter(
            start_date__range=(
                datetime(year, month, 1), datetime(year, month + 1, calendar.monthrange(year, month + 1)[1]))).order_by(
            'start_date')
        for i in range(31):
            each_date = today+timedelta(days=i)
            event_dates.append([each_date])
            for event in events:
                if event.end_date.month == each_date.month:
                    if (event.start_date.day <= each_date.day) and (event.end_date.day >= each_date.day):
                        event_dates[i].append(event)
        
        for i in range(31):
            each_date = today+timedelta(days=i)
            event_dates.append([each_date])
            for event in events:
                if event.end_date.month + 1 == each_date.month:
                    if event.start_date.day <= each_date.day:
                        event_dates[i].append(event)
                
        response['events'] = event_dates
        try:
            notice = Board.objects.get(name='공지사항')

            response['recent_posts'] = Post.objects.exclude(board=notice) \
                                           .order_by('-write_date')[:3]
            response['notice_posts'] = notice.post_set.order_by('-emphasis')[:3]
            response['notice'] = Notice.objects.all()[0]
        except Board.DoesNotExist:
            notice = None
        except IndexError:
            pass
        return render(request, self.template_name, response)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        if not data.get('email'):
            return redirect('/profile?error=이메일을 입력해주세요')

        user = request.user

        user.email = data.get('email')
        user.phone = data.get('phone', '')
        user.sns = data.get('sns', '')
        user.save()

        return redirect('profile')


class SignUpView(TemplateView):
    template_name = 'sign_up.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        
        if not (data.get('name') and data.get('password') and data.get('user_id') and data.get('Email')
                and data.get('phone') and data.get('period') and data.get('enter_year')):
            return redirect('/sign_up?error=회원 가입에 필요한 정보가 부족합니다.')

        member = Member()
        member.user_id = data.get('user_id')
        member.name = data.get('name')
        member.set_password(data.get('password'))
        member.email = data.get('Email')
        member.phone = data.get('phone')
        member.period = data.get('period')
        member.enter_year = data.get('enter_year')

        try:
            member.grade = Grade.objects.get(name='미승인')
        except ObjectDoesNotExist:
            return redirect('/sign_up?error=해당 등급이 존재하지 않습니다.')

        try:
            member.save()
        except IntegrityError:
            return render(request, 'sign_up.html', {"message": "같은 아이디가 존재합니다."})

        return redirect('/login?success=회원 가입이 완료되었습니다.')


class SitemapView(TemplateView):
    template_name = 'sitemap.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)


class TermsAndConditionsView(TemplateView):
    template_name = 'terms_and_conditions.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)