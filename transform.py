import pandas as pd
from datetime import datetime


def parse_match_data(match_data):
    """
    @TODO make modular
    Parse and transform raw match data into structured dataframes."""
    parsed_data = {
        "basic_info": [],
        "goal_stats": [],
        "corner_stats": [],
        "referee_stats": [],
        "probability_stats": [],
        "form_stats": [],
        "offside_stats": [],
        "top_scorers": [],
        "goal_times": [],
        "half_time_stats": [],
        "facts": [],
        "over_under_stats": []
    }

    for match_uuid, match_data in match_data.items():
        try:
            # Ana veri objelerini al
            match = match_data['data']['match']
            competition = match_data['data']['competition']
            season = match_data['data']['season']
            h2h = match_data['data'].get('h2h', {})
            probabilities = match_data['data'].get('mr_probabilities', {})
            forms = match_data['data'].get('forms', {})
            teams_stats = match_data['data'].get('teams_stats', {})

            def get_team_stat(team_stats, stat_name):
                return float(next((stat['value'] for stat in team_stats if stat['name'] == stat_name), 0))

            team_A_stats = teams_stats['general']['match_averages'][0]['team_A']['stats']
            team_B_stats = teams_stats['general']['match_averages'][0]['team_B']['stats']

            # 1. Temel Maç Bilgileri
            basic_match_info = {
                'mac': f"{match['team_A']['display_name']}-{match['team_B']['display_name']}",
                'lig': competition['name'],
                'sezon': season['name'],
                'stadyum': match['venue']['name'],
                'tarih': datetime.strptime(match['date_time_utc'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
                'mac_saati': match['match_time'],
                'hafta': match['match_day'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name']
            }

            # 2. Gol İstatistikleri
            goal_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                # Mevcut form istatistikleri
                'ev_sahibi_lig_son_5_mac_attigi_gol': forms['team_A']['competition'].get('goal_pro', 0),
                'ev_sahibi_lig_son_5_mac_yedigi_gol': forms['team_A']['competition'].get('goal_against', 0),
                'ev_sahibi_ic_saha_son_5_mac_attigi_gol': forms['team_A']['competition_home'].get('goal_pro', 0),
                'ev_sahibi_ic_saha_son_5_mac_yedigi_gol': forms['team_A']['competition_home'].get('goal_against', 0),
                'deplasman_lig_son_5_mac_attigi_gol': forms['team_B']['competition'].get('goal_pro', 0),
                'deplasman_lig_son_5_mac_yedigi_gol': forms['team_B']['competition'].get('goal_against', 0),
                'deplasman_dis_saha_son_5_mac_attigi_gol': forms['team_B']['competition_away'].get('goal_pro', 0),
                'deplasman_dis_saha_son_5_mac_yedigi_gol': forms['team_B']['competition_away'].get('goal_against', 0),

                # Şut ortalamaları
                'ev_sahibi_sut_ortalamasi': get_team_stat(team_A_stats, 'Ave_shots_per_game'),
                'deplasman_sut_ortalamasi': get_team_stat(team_B_stats, 'Ave_shots_per_game'),

                # Sezon gol ortalamaları
                'ev_sahibi_sezon_mac_basi_atilan_gol_ort': float(
                    teams_stats['goal']['average_goals'][0]['team_A']['stats'][0]['value']),
                'ev_sahibi_sezon_mac_basi_yenilen_gol_ort': float(
                    teams_stats['goal']['average_goals'][0]['team_A']['stats'][1]['value']),
                'deplasman_sezon_mac_basi_atilan_gol_ort': float(
                    teams_stats['goal']['average_goals'][0]['team_B']['stats'][0]['value']),
                'deplasman_sezon_mac_basi_yenilen_gol_ort': float(
                    teams_stats['goal']['average_goals'][0]['team_B']['stats'][1]['value']),

                # Gol dağılımları
                'ev_sahibi_0_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_A']['stats'][0]['value']),
                'ev_sahibi_1_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_A']['stats'][1]['value']),
                'ev_sahibi_2_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_A']['stats'][2]['value']),
                'ev_sahibi_3_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_A']['stats'][3]['value']),
                'ev_sahibi_4_plus_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_A']['stats'][4]['value']),

                'deplasman_0_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_B']['stats'][0]['value']),
                'deplasman_1_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_B']['stats'][1]['value']),
                'deplasman_2_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_B']['stats'][2]['value']),
                'deplasman_3_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_B']['stats'][3]['value']),
                'deplasman_4_plus_gol_mac_sayisi': int(
                    teams_stats['goal']['goals_per_game'][0]['team_B']['stats'][4]['value'])
            }

            # 3. Korner İstatistikleri
            corner_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                'ev_sahibi_korner_ortalamasi': get_team_stat(team_A_stats, 'Ave_corners_per_game'),
                'deplasman_korner_ortalamasi': get_team_stat(team_B_stats, 'Ave_corners_per_game'),
                'toplam_korner_ortalamasi': get_team_stat(team_A_stats, 'Ave_corners_per_game') + get_team_stat(
                    team_B_stats, 'Ave_corners_per_game')
            }

            # 4. Hakem İstatistikleri
            referee_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                'hakem': next((ref['name'] for ref in match['referees'] if ref['type'] == 'Main'), 'Atanmadı'),
                'hakem_ortalama_sari_kart': float(match['referee'].get('avg_yc', 0)),
                'hakem_ortalama_kirmizi_kart': float(match['referee'].get('avg_rc', 0)),
                'ev_sahibi_faul_ortalamasi': get_team_stat(team_A_stats, 'Ave_fouls_per_game'),
                'deplasman_faul_ortalamasi': get_team_stat(team_B_stats, 'Ave_fouls_per_game')
            }

            # 5. Tahmin ve Olasılık İstatistikleri
            probability_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                'ev_sahibi_kazanma_olasiligi': probabilities.get('home', 0),
                'beraberlik_olasiligi': probabilities.get('draw', 0),
                'deplasman_kazanma_olasiligi': probabilities.get('away', 0)
            }

            # 6. Form ve Seri İstatistikleri
            form_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                'ev_sahibi_lig_son_5_mac_serisi': forms['team_A']['competition'].get('serie', ''),
                'ev_sahibi_ic_saha_son_5_mac_serisi': forms['team_A']['competition_home'].get('serie', ''),
                'deplasman_lig_son_5_mac_serisi': forms['team_B']['competition'].get('serie', ''),
                'deplasman_dis_saha_son_5_mac_serisi': forms['team_B']['competition_away'].get('serie', ''),

                # Son Karşılaşma İstatistikleri
                'aralarindaki_son_10_mac_karsilikli_gol_olan_mac_sayisi': h2h.get('both_score', 0),
                'aralarindaki_son_10_mac_beraberlik_sayisi': h2h.get('draw', 0),
                'aralarindaki_son_10_mac_2_5_gol_ustu_olan_mac_sayisi': h2h.get('goal_over', 0),
                'aralarindaki_son_10_mac_ev_sahibi_gol_sayisi': h2h.get('team_A', {}).get('goal_pro', 0),
                'aralarindaki_son_10_mac_ev_sahibi_galibiyet_sayisi': h2h.get('team_A', {}).get('win', 0),
                'aralarindaki_son_10_mac_deplasman_gol_sayisi': h2h.get('team_B', {}).get('goal_pro', 0),
                'aralarindaki_son_10_mac_deplasman_galibiyet_sayisi': h2h.get('team_B', {}).get('win', 0)
            }

            # 7. Diğer Maç İstatistikleri
            offside_stats = {
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                'mac': basic_match_info['mac'],
                'ev_sahibi_ofsayt_ortalamasi': get_team_stat(team_A_stats, 'Ave_offsides_per_game'),
                'deplasman_ofsayt_ortalamasi': get_team_stat(team_B_stats, 'Ave_offsides_per_game'),
            }

            # 8. En golcü oyuncular için ayrı bir sözlük
            top_scorers_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                # Ev sahibi takımın golcüleri (ilk 5)
                'ev_sahibi_golcu_1': f"{teams_stats['goal']['top_goalscorers'][0]['team_A']['stats'][0]['player']['name']} ({int(teams_stats['goal']['top_goalscorers'][0]['team_A']['stats'][0]['value'])} gol)",
                'ev_sahibi_golcu_2': f"{teams_stats['goal']['top_goalscorers'][0]['team_A']['stats'][1]['player']['name']} ({int(teams_stats['goal']['top_goalscorers'][0]['team_A']['stats'][1]['value'])} gol)",
                'ev_sahibi_golcu_3': f"{teams_stats['goal']['top_goalscorers'][0]['team_A']['stats'][2]['player']['name']} ({int(teams_stats['goal']['top_goalscorers'][0]['team_A']['stats'][2]['value'])} gol)",

                # Deplasman takımının golcüleri (ilk 5)
                'deplasman_golcu_1': f"{teams_stats['goal']['top_goalscorers'][0]['team_B']['stats'][0]['player']['name']} ({int(teams_stats['goal']['top_goalscorers'][0]['team_B']['stats'][0]['value'])} gol)",
                'deplasman_golcu_2': f"{teams_stats['goal']['top_goalscorers'][0]['team_B']['stats'][1]['player']['name']} ({int(teams_stats['goal']['top_goalscorers'][0]['team_B']['stats'][1]['value'])} gol)",
                'deplasman_golcu_3': f"{teams_stats['goal']['top_goalscorers'][0]['team_B']['stats'][2]['player']['name']} ({int(teams_stats['goal']['top_goalscorers'][0]['team_B']['stats'][2]['value'])} gol)",
            }

            # Yarı İstatistikleri Tablosu
            half_time_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                # Ev sahibi ilk yarı golleri (0-45)
                'ev_sahibi_ilk_yari_attigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][6]['value']) +  # 0-15
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][7]['value']) +  # 16-30
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][8]['value'])  # 31-45
                ),
                'ev_sahibi_ilk_yari_yedigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][0]['value']) +  # 0-15
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][1]['value']) +  # 16-30
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][2]['value'])  # 31-45
                ),

                # Ev sahibi ikinci yarı golleri (46-90)
                'ev_sahibi_ikinci_yari_attigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][9]['value']) +  # 46-60
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][10]['value']) +  # 61-75
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][11]['value'])  # 76-90
                ),
                'ev_sahibi_ikinci_yari_yedigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][3]['value']) +  # 46-60
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][4]['value']) +  # 61-75
                        int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][5]['value'])  # 76-90
                ),

                # Deplasman ilk yarı golleri (0-45)
                'deplasman_ilk_yari_attigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][6]['value']) +  # 0-15
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][7]['value']) +  # 16-30
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][8]['value'])  # 31-45
                ),
                'deplasman_ilk_yari_yedigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][0]['value']) +  # 0-15
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][1]['value']) +  # 16-30
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][2]['value'])  # 31-45
                ),

                # Deplasman ikinci yarı golleri (46-90)
                'deplasman_ikinci_yari_attigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][9]['value']) +  # 46-60
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][10]['value']) +  # 61-75
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][11]['value'])  # 76-90
                ),
                'deplasman_ikinci_yari_yedigi': (
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][3]['value']) +  # 46-60
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][4]['value']) +  # 61-75
                        int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][5]['value'])  # 76-90
                )
            }

            # Facts istatistiklerini ekle
            facts_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                'fact1': '',
                'fact2': '',
                'fact3': '',
                'fact4': '',
                'fact5': ''
            }

            # Mevcut facts'leri sözlüğe ekle
            facts_list = match_data['data'].get('facts', [])
            for i, fact in enumerate(facts_list[:5]):  # İlk 5 fact'i al
                facts_stats[f'fact{i + 1}'] = fact['fact']

            # parsed_data sözlüğüne facts kategorisini ekle
            if 'facts' not in parsed_data:
                parsed_data['facts'] = []

            # Veriyi listeye ekle
            parsed_data['facts'].append(facts_stats)

            # Her kategorideki verileri ilgili listeye ekle
            parsed_data['basic_info'].append(basic_match_info)
            parsed_data['goal_stats'].append(goal_stats)
            parsed_data['corner_stats'].append(corner_stats)
            parsed_data['referee_stats'].append(referee_stats)
            parsed_data['probability_stats'].append(probability_stats)
            parsed_data['form_stats'].append(form_stats)
            parsed_data['offside_stats'].append(offside_stats)
            parsed_data['top_scorers'].append(top_scorers_stats)
            parsed_data['half_time_stats'].append(half_time_stats)

            # Add over/under stats dictionary
            over_under_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                
                # Team A (Home) over/under stats
                'ev_sahibi_0_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_A'][0]['o']),
                'ev_sahibi_0_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_A'][0]['u']),
                'ev_sahibi_1_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_A'][1]['o']),
                'ev_sahibi_1_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_A'][1]['u']),
                'ev_sahibi_2_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_A'][2]['o']),
                'ev_sahibi_2_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_A'][2]['u']),
                'ev_sahibi_3_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_A'][3]['o']),
                'ev_sahibi_3_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_A'][3]['u']),
                'ev_sahibi_4_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_A'][4]['o']),
                'ev_sahibi_4_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_A'][4]['u']),
                
                # Team B (Away) over/under stats
                'deplasman_0_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_B'][0]['o']),
                'deplasman_0_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_B'][0]['u']),
                'deplasman_1_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_B'][1]['o']),
                'deplasman_1_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_B'][1]['u']),
                'deplasman_2_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_B'][2]['o']),
                'deplasman_2_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_B'][2]['u']),
                'deplasman_3_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_B'][3]['o']),
                'deplasman_3_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_B'][3]['u']),
                'deplasman_4_5_alti_mac_sayisi': int(match_data['data']['statistics']['team_B'][4]['o']),
                'deplasman_4_5_ustu_mac_sayisi': int(match_data['data']['statistics']['team_B'][4]['u'])
            }

            # Add over_under_stats to parsed_data
            parsed_data['over_under_stats'].append(over_under_stats)

            # Add back the goal_times_stats dictionary after top_scorers_stats
            goal_times_stats = {
                'mac': basic_match_info['mac'],
                'ev_sahibi': match['team_A']['display_name'],
                'deplasman': match['team_B']['display_name'],
                # Ev sahibi yediği goller (dakika aralıklarına göre)
                'ev_sahibi_0_15_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][0]['value']),
                'ev_sahibi_16_30_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][1]['value']),
                'ev_sahibi_31_45_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][2]['value']),
                'ev_sahibi_46_60_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][3]['value']),
                'ev_sahibi_61_75_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][4]['value']),
                'ev_sahibi_76_90_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][5]['value']),

                # Ev sahibi attığı goller (dakika aralıklarına göre)
                'ev_sahibi_0_15_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][6]['value']),
                'ev_sahibi_16_30_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][7]['value']),
                'ev_sahibi_31_45_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][8]['value']),
                'ev_sahibi_46_60_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][9]['value']),
                'ev_sahibi_61_75_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][10]['value']),
                'ev_sahibi_76_90_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][11]['value']),

                # Ev sahibi ortalama gol dakikaları
                'ev_sahibi_son_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][12]['value'],
                'ev_sahibi_ilk_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][13]['value'],
                'ev_sahibi_ilk_yedigi_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][14]['value'],
                'ev_sahibi_son_yedigi_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_A']['stats'][15]['value'],

                # Deplasman yediği goller (dakika aralıklarına göre)
                'deplasman_0_15_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][0]['value']),
                'deplasman_16_30_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][1]['value']),
                'deplasman_31_45_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][2]['value']),
                'deplasman_46_60_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][3]['value']),
                'deplasman_61_75_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][4]['value']),
                'deplasman_76_90_yedigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][5]['value']),

                # Deplasman attığı goller (dakika aralıklarına göre)
                'deplasman_0_15_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][6]['value']),
                'deplasman_16_30_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][7]['value']),
                'deplasman_31_45_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][8]['value']),
                'deplasman_46_60_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][9]['value']),
                'deplasman_61_75_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][10]['value']),
                'deplasman_76_90_attigi': int(teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][11]['value']),

                # Deplasman ortalama gol dakikaları
                'deplasman_son_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][12]['value'],
                'deplasman_ilk_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][13]['value'],
                'deplasman_ilk_yedigi_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][14]['value'],
                'deplasman_son_yedigi_gol_ort_dk': teams_stats['goal']['time_of_goals'][0]['team_B']['stats'][15]['value']
            }

            # Add back the append operation in the data collection section
            parsed_data['goal_times'].append(goal_times_stats)

        except KeyError as e:
            print(f"KeyError while parsing match {match_uuid}: {e}")
            continue

    # Convert lists to DataFrames
    return {category: pd.DataFrame(data) for category, data in parsed_data.items() if data}