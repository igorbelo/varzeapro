from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from core.models import (Profile, Match, Team,\
                         State, City, Position, Athlete,\
                         StatType, MatchStat, Arena, Attribute, AthleteAttribute)
from random import randint
import math
import uuid
from tqdm import tqdm
from datetime import datetime, timedelta
from random import randint, uniform
from multiprocessing import Process
from django import db

NUMBER_OF_STATES = 26
NUMBER_OF_CITIES = 70
NUMBER_OF_TEAMS = 1000
NUMBER_OF_ATHLETES_IN_TEAM = 11
NUMBER_OF_ATHLETES = NUMBER_OF_TEAMS * NUMBER_OF_ATHLETES_IN_TEAM
NUMBER_OF_ARENAS = 20
NUMBER_OF_MATCHES = 200000
POSITIONS_LIST = (
    'Goleiro','Lateral','Zagueiro','Volante','Meio-campo','Atacante'
)
fake = Faker()

def bulk_create_matches(matches):
    Match.objects.bulk_create(matches)

def bulk_create_stats(stats):
    MatchStat.objects.bulk_create(stats)

def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))

def random_distr(l):
    r = uniform(0, 1)
    s = 0
    for item, prob in l:
        s += prob
        if s >= r:
            return item
    return item

bad_attribute = [
    (1, 0.5),
    (2, 0.15),
    (3, 0.15),
    (4, 0.15),
    (5, 0.05)
]
not_too_bad_attribute = [
    (1, 0.15),
    (2, 0.5),
    (3, 0.15),
    (4, 0.10),
    (5, 0.10)
]
avg_attribute = [
    (1, 0.10),
    (2, 0.15),
    (3, 0.5),
    (4, 0.15),
    (5, 0.10)
]
good_attribute = [
    (1, 0.05),
    (2, 0.10),
    (3, 0.2),
    (4, 0.5),
    (5, 0.15)
]
great_attribute = [
    (1, 0.05),
    (2, 0.15),
    (3, 0.15),
    (4, 0.15),
    (5, 0.5)
]


def attribute_for_position(attr, position):
    if attr == 'physique':
        if position.name == 'Goleiro':
            return random_distr(good_attribute)
        elif position.name == 'Zagueiro':
            return random_distr(great_attribute)
        elif position.name == 'Lateral':
            return random_distr(good_attribute)
        elif position.name == 'Volante':
            return random_distr(good_attribute)
        elif position.name == 'Meio-campo':
            return random_distr(not_too_bad_attribute)
        else:
            return random_distr(good_attribute)
    elif attr == 'intelligence':
        if position.name == 'Goleiro':
            return random_distr(avg_attribute)
        elif position.name == 'Zagueiro':
            return random_distr(not_too_bad_attribute)
        elif position.name == 'Lateral':
            return random_distr(avg_attribute)
        elif position.name == 'Volante':
            return random_distr(avg_attribute)
        elif position.name == 'Meio-campo':
            return random_distr(great_attribute)
        else:
            return random_distr(great_attribute)
    elif attr == 'technique':
        if position.name == 'Goleiro':
            return random_distr(good_attribute)
        elif position.name == 'Zagueiro':
            return random_distr(avg_attribute)
        elif position.name == 'Lateral':
            return random_distr(avg_attribute)
        elif position.name == 'Volante':
            return random_distr(not_too_bad_attribute)
        elif position.name == 'Meio-campo':
            return random_distr(great_attribute)
        else:
            return random_distr(good_attribute)
    else:
        if position.name == 'Goleiro':
            return random_distr(bad_attribute)
        elif position.name == 'Zagueiro':
            return random_distr(bad_attribute)
        elif position.name == 'Lateral':
            return random_distr(good_attribute)
        elif position.name == 'Volante':
            return random_distr(avg_attribute)
        elif position.name == 'Meio-campo':
            return random_distr(good_attribute)
        else:
            return random_distr(great_attribute)

class Command(BaseCommand):
    def handle(self, *args, **options):
        # attributes = []
        # for attr in ('speed', 'technique', 'intelligence', 'physique'):
        #     attributes.append(Attribute.objects.create(name = attr))

        # for athlete in Athlete.objects.all():
        #     for attr in attributes:
        #         AthleteAttribute.objects.create(
        #             athlete = athlete,
        #             attribute = attr,
        #             value = attribute_for_position(attr.name, athlete.position)
        #         )

        for match_stat in MatchStat.objects.filter(athlete__position__name__in = ['Goleiro'], type_id = 1):
            match_stat.delete()

        for athlete in Athlete.objects.all():
            if athlete.position.name == 'Atacante':
                for i in range(randint(50, 100)):
                    MatchStat.objects.create(
                        athlete = athlete,
                        team = athlete.team,
                        type_id = 1,
                        match_id = randint(1, 200000)
                    )
            elif athlete.position.name == 'Meio-campo':
                for i in range(randint(25, 50)):
                    MatchStat.objects.create(
                        athlete = athlete,
                        team = athlete.team,
                        type_id = 1,
                        match_id = randint(1, 200000)
                    )
            elif athlete.position.name == 'Volante':
                for i in range(randint(10, 25)):
                    MatchStat.objects.create(
                        athlete = athlete,
                        team = athlete.team,
                        type_id = 1,
                        match_id = randint(1, 200000)
                    )
            elif athlete.position.name == 'Zagueiro':
                for i in range(randint(0, 10)):
                    MatchStat.objects.create(
                        athlete = athlete,
                        team = athlete.team,
                        type_id = 1,
                        match_id = randint(1, 200000)
                    )
            elif athlete.position.name == 'Lateral':
                for i in range(randint(0, 10)):
                    MatchStat.objects.create(
                        athlete = athlete,
                        team = athlete.team,
                        type_id = 1,
                        match_id = randint(1, 200000)
                    )


        # # stat types
        # STAT_TYPES_LIST = (
        #     'goal','own-goal','yellow-card','red-card'
        # )
        # stat_types = []
        # for stat_name in STAT_TYPES_LIST:
        #     stat_types.append(
        #         StatType.objects.create(
        #             name = stat_name
        #         )
        #     )
        # # positions
        # self.positions = []
        # for position_name in POSITIONS_LIST:
        #     self.positions.append(
        #         Position.objects.create(
        #             name = position_name
        #         )
        #     )
        # # states
        # states = []
        # for _ in range(0,NUMBER_OF_STATES):
        #     state_name = fake.state()
        #     states.append(
        #         State.objects.create(
        #             name = state_name
        #         )
        #     )
        # # cities
        # cities = []
        # for _ in range(0,NUMBER_OF_CITIES):
        #     city_name = fake.city()
        #     cities.append(
        #         City.objects.create(
        #             name = city_name,
        #             state = states[
        #                 randint(0,NUMBER_OF_STATES-1)
        #             ]
        #         )
        #     )
        # # teams
        # print "criando times..."
        # self.teams = []
        # for _ in tqdm(range(0,NUMBER_OF_TEAMS)):
        #     team_city = cities[
        #         randint(0,NUMBER_OF_CITIES-1)
        #     ]
        #     team_name = fake.company()
        #     self.teams.append(
        #         Team(
        #             city = team_city,
        #             name = team_name
        #         )
        #     )
        # Team.objects.bulk_create(self.teams)
        # # athletes
        # print "criando atletas..."
        # users = []
        # profiles = []
        # athletes = []

        # for i in tqdm(range(NUMBER_OF_ATHLETES)):
        #     first_name = "FakeFirstName"
        #     last_name = "FakeLastName"
        #     email = str(uuid.uuid1())+"@varzeapro.com"
        #     user = User(
        #         first_name = first_name,
        #         last_name = last_name,
        #         email = email,
        #         username = email
        #     )
        #     users.append(user)
        #     d1 = datetime.strptime('1/1/1970', '%m/%d/%Y')
        #     d2 = datetime.strptime('10/1/1998', '%m/%d/%Y')
        #     when = random_date(d1, d2)
        #     profile = Profile(
        #         user_id = i+1,
        #         birthday = when
        #     )
        #     profiles.append(profile)
        #     team_index = int(
        #         math.floor(i/NUMBER_OF_ATHLETES_IN_TEAM)
        #     )
        #     team = self.teams[team_index]
        #     position = self.positions[
        #         randint(0,len(POSITIONS_LIST)-1)
        #     ]
        #     athlete = Athlete(
        #         profile_id = i+1,
        #         team = team,
        #         position = position
        #     )
        #     athletes.append(athlete)

        # User.objects.bulk_create(users)
        # Profile.objects.bulk_create(profiles)
        # Athlete.objects.bulk_create(athletes)
        # # arenas
        # arenas = []
        # for i in range(0,NUMBER_OF_ARENAS):
        #     arenas.append(
        #         Arena.objects.create(
        #             name = fake.street_name()
        #         )
        #     )
        # # matches
        # print "criando partidas..."
        # matches = []
        # stats = []
        # for i in tqdm(range(0,NUMBER_OF_MATCHES)):
        #     home_team_index = int(
        #         math.floor(i/200)
        #     )
        #     visitor_team_index = randint(0,NUMBER_OF_TEAMS-1)
        #     if visitor_team_index == team_index:
        #         if visitor_team_index == 0:
        #             visitor_team_index += 1
        #         else:
        #             visitor_team_index -= 1

        #     if i % 2 != 0:
        #         c = home_team_index
        #         home_team_index = visitor_team_index
        #         visitor_team_index = c

        #     home_team_id = home_team_index+1
        #     visitor_team_id = visitor_team_index+1

        #     arena = arenas[randint(0,NUMBER_OF_ARENAS-1)]
        #     d1 = datetime.strptime('1/1/2010 7:00 AM', '%m/%d/%Y %I:%M %p')
        #     d2 = datetime.strptime('10/1/2016 4:00 PM', '%m/%d/%Y %I:%M %p')
        #     when = random_date(d1, d2)
        #     matches.append(
        #         Match(
        #             arena = arena,
        #             home_team_id = home_team_id,
        #             visitor_team_id = visitor_team_id,
        #             when = when
        #         )
        #     )
        #     home_team_score = randint(0,7)
        #     visitor_team_score = randint(0,7)
        #     for j in range(home_team_score):
        #         if randint(0,20) == 5:
        #             start_index_athlete = visitor_team_index * 11
        #             end_index_athlete = start_index_athlete + 10
        #             random_athlete_id = randint(start_index_athlete, end_index_athlete)+1
        #             stats.append(
        #                 MatchStat(
        #                     match_id = i+1,
        #                     team_id = visitor_team_id,
        #                     athlete_id = random_athlete_id,
        #                     type = stat_types[1]
        #                 )
        #             )
        #         else:
        #             start_index_athlete = home_team_index * 11
        #             end_index_athlete = start_index_athlete + 10
        #             random_athlete_id = randint(start_index_athlete, end_index_athlete)+1
        #             stats.append(
        #                 MatchStat(
        #                     match_id = i+1,
        #                     team_id = home_team_id,
        #                     athlete_id = random_athlete_id,
        #                     type = stat_types[0]
        #                 )
        #             )

        #     for j in range(visitor_team_score):
        #         if randint(0,20) == 5:
        #             start_index_athlete = home_team_index * 11
        #             end_index_athlete = start_index_athlete + 10
        #             random_athlete_id = randint(start_index_athlete, end_index_athlete)+1
        #             stats.append(
        #                 MatchStat(
        #                     match_id = i+1,
        #                     team_id = home_team_id,
        #                     athlete_id = random_athlete_id,
        #                     type = stat_types[1]
        #                 )
        #             )
        #         else:
        #             start_index_athlete = visitor_team_index * 11
        #             end_index_athlete = start_index_athlete + 10
        #             random_athlete_id = randint(start_index_athlete, end_index_athlete)+1
        #             stats.append(
        #                 MatchStat(
        #                     match_id = i+1,
        #                     team_id = visitor_team_id,
        #                     athlete_id = random_athlete_id,
        #                     type = stat_types[0]
        #                 )
        #             )

        # processes = []
        # db.connections.close_all()

        # for i in range(4):
        #     start_index = i * (NUMBER_OF_MATCHES/4)
        #     end_index = start_index + (NUMBER_OF_MATCHES/4)
        #     matches_range = matches[start_index:end_index]
        #     p = Process(target=bulk_create_matches, args=(matches_range,))
        #     p.start()
        #     processes.append(p)

        # for p in processes:
        #     p.join()

        # print "criando resultados..."
        # stats_length = len(stats)
        # for i in range(4):
        #     start_index = i * (stats_length/4)
        #     end_index = start_index + (stats_length/4)
        #     stats_range = stats[start_index:end_index]
        #     p = Process(target=bulk_create_stats, args=(stats_range,))
        #     p.start()
        #     processes.append(p)

        # for p in processes:
        #     p.join()
