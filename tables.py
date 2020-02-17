def s_table(value)
    table = 
        {
        1:-5,
        2:-4,
        3:-4,
        4:-3,
        5:-3,
        6:-2,
        7:-2,
        8:-1,
        9:-1,
        10:0,
        11:0,
        12:1,
        13:1,
        14:2,
        15:2,
        16:3,
        17:3,
        18:4,
        19:4,
        20:5,
        21:5,
        22:6,
        23:6,
        24:7,
        25:7,
        26:8,
        27:8,
        28:9,
        29:9,
        30:10
        }
    return table[value]

def l_table(level, value, char)
    table = 
        {
        E.xperience:  
            {
            0: {team.PC: -1,
                team.Mob:10
                },
            1/8:{team.PC: -1,
                team.Mob:25
                },
            1/4:{team.PC: -1,
                team.Mob:50
                },
            1/2:{team.PC: -1,
                team.Mob:100
                },
            1:  {team.PC: 0,
                team.Mob:200
                },
            2:  {team.PC: 300,
                team.Mob:450
                },
            3:  {team.PC: 900,
                team.Mob:700
                },
            4:  {team.PC: 2700,
                team.Mob:1100
                },
            5:  {team.PC: 6500,
                team.Mob:1500
                },
            6:  {team.PC: 14000,
                team.Mob:2300
                },
            7:  {team.PC: 23000,
                team.Mob:2900
                },
            8:  {team.PC: 34000,
                team.Mob:3900
                },
            9:  {team.PC: 48000,
                team.Mob:5000
                },
            10: {team.PC: 64000,
                team.Mob: 5900
                },
            11: {team.PC: 85000,
                team.Mob:7200
                },
            12: {team.PC: 100000,
                team.Mob:8400
                },
            13: {team.PC: 120000,
                team.Mob:10000
                },
            14: {team.PC: 140000,
                team.Mob:11500
                },
            15: {team.PC: 165000,
                team.Mob:13000
                },
            16: {team.PC: 195000,
                team.Mob:15000
                },
            17: {team.PC: 225000,
                team.Mob:18000
                },
            18: {team.PC: 265000,
                team.Mob:20000
                },
            19: {team.PC: 305000,
                team.Mob:22000
                },
            20: {team.PC: 355000,
                team.Mob: 25000
                }
            21: {team.PC: -1,
                team.Mob:33000
                }
            22: {team.PC: -1,
                team.Mob:41000
                }
            23: {team.PC: -1,
                team.Mob:50000
                }
            24: {team.PC: -1,
                team.Mob:62000
                }
            30: {team.PC: -1,
                team.Mob:155000
                }    
            },
        Skill.Proficiency:
            {
            0: {team.PC: -1,
                team.Mob: 2
                },
            1/8:{team.PC: -1,
                team.Mob: 2
                },
            1/4:{team.PC: -1,
                team.Mob: 2
                },
            1/2:{team.PC: -1,
                team.Mob: 2
                },
            1:  {team.PC: 2,
                team.Mob:
                },
            2:  {team.PC: 2,
                team.Mob:
                },
            3:  {team.PC: 2,
                team.Mob: 2
                },
            4:  {team.PC: 2,
                team.Mob: 2
                },
            5:  {team.PC: 3,
                team.Mob: 3
                },
            6:  {team.PC: 3,
                team.Mob: 3
                },
            7:  {team.PC: 3,
                team.Mob: 3
                },
            8:  {team.PC: 3,
                team.Mob: 3
                },
            9:  {team.PC: 4,
                team.Mob: 4
                },
            10: {team.PC: 4,
                team.Mob:
                },
            11: {team.PC: 4,
                team.Mob: 4
                },
            12: {team.PC: 4,
                team.Mob:
                },
            13: {team.PC: 5,
                team.Mob: 5
                },
            14: {team.PC: 5,
                team.Mob:
                },
            15: {team.PC: 5,
                team.Mob:
                },
            16: {team.PC: 5,
                team.Mob:
                },
            17: {team.PC: 6,
                team.Mob:
                },
            18: {team.PC: 6,
                team.Mob:
                },
            19: {team.PC: 6,
                team.Mob:
                },
            20: {team.PC: 6,
                team.Mob:
                }  
            21: {team.PC: -1,
                team.Mob: 7
                }
            22: {team.PC: -1,
                team.Mob: 7
                }
            23: {team.PC: -1,
                team.Mob: 7
                }
            24: {team.PC: -1,
                team.Mob: 7
                }
            30: {team.PC: -1,
                team.Mob: 9
                }
            }
        }
    return table[value][level][char]
