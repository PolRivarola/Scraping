import scraping_accuweather as accuw
import scraping_bug as bug
import matplotlib.pyplot as plt

def compare_sites(stats, date):

    print(f"max accu {stats[0]['highs']}")
    print(f"max bug {stats[1]['highs']}")
    
    print(f"min accu {stats[0]['lows']}")
    print(f"min bug {stats[1]['lows']}")
    
    print(f"min accu {stats[0]['days']}")
    print(f"min bug {stats[1]['days']}")
    
    plt.figure(figsize=(12, 6))

    plt.plot(stats[0]['days'], stats[0]['highs'], marker='o', linestyle='-', label='High Temp Accuweather (°F)', color='red')
    plt.plot(stats[1]['days'], stats[1]['highs'], marker='o', linestyle='--', label='High Temp WeatherBug (°F)', color='red')
    
    plt.plot(stats[0]['days'], stats[0]['lows'], marker='o', linestyle='-', label='Low Temp Accuweather (°F)', color='blue')
    plt.plot(stats[1]['days'], stats[1]['lows'], marker='o', linestyle='--', label='Low Temp WeatherBug(°F)', color='blue')
    
    avg_highs = [(h1 + h2) / 2 for h1, h2 in zip(stats[0]['highs'], stats[1]['highs'])]
    avg_lows = [(l1 + l2) / 2 for l1, l2 in zip(stats[0]['lows'], stats[1]['lows'])]
    
    plt.plot(stats[0]['days'], avg_highs, marker='o', linestyle='-', label='Avg High Temp (°F)', color='green')
    plt.plot(stats[0]['days'], avg_lows, marker='o', linestyle='-', label='Avg Low Temp (°F)', color='purple')

    for i in range(len(avg_highs)):
        plt.text((stats[0]['days'][i])-0.15, avg_highs[i]    , f"{avg_highs[i]:.1f}°", fontsize=8, color='black', ha='center')
        plt.text((stats[0]['days'][i])-0.15, avg_lows[i] , f"{avg_lows[i]:.1f}°", fontsize=8, color='black', ha='center')


    plt.xlabel(f'Days of {date["month"]}, {date["year"]}')
    plt.ylabel('Temperature (°F)')
    plt.title('Temperature Evolution')

    plt.xticks(stats[0]['days'], rotation=45)

    plt.ylim(int(min(min(stats[0]['lows']),min(stats[1]['lows']))) - 1, int(max(max(stats[0]['highs']),max(stats[1]['highs']))) + 1)

    plt.tight_layout()

    plt.legend()

    plt.show()

stats, date  = accuw.get_data_accu()
stats2, date2  = bug.get_data_bug()

compare_sites([stats,stats2],date)
