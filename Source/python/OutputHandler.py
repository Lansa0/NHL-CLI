from datetime import datetime
import os

# TODO
# Put each row string in a list and join together, rather then adding to
# a new string

def _formatStandings(data : dict, args) -> str:
    """
    Formats standings data for output

    data : dict
        Standings data. See samples/standings.json for structure reference

    args : argparse.Namespace
        Given user input. Only using args.type from this to show what the 
        user wants to see.
        Valid type inputs:
        - division
        - conference
        - league (empty or non valid types defualt to this)

    return str
        Formatted standings output
    """

    Template_Row : str = "|{Position}| {Team}|{GP}|{Wins}|{Losses}|{Overtime}|{Points}|{Differential}|{Home}|{Away}|{Streak}|\n"
    def formatTeamRow(team_data : dict, position_sort : str = "leagueSequence") -> str:
        return Template_Row.format(
            Position        = str(team_data[position_sort]).center(5),
            Team            = team_data["teamName"]["default"].ljust(24),
            GP              = str(team_data["gamesPlayed"]).center(4),
            Wins            = str(team_data["wins"]).center(3),
            Losses          = str(team_data["losses"]).center(3),
            Overtime        = str(team_data["otLosses"]).center(4),
            Points          = str(team_data["points"]).center(5),
            Differential    = str(team_data["goalDifferential"]).center(6),
            Home            = f"{team_data["homeWins"]}-{team_data["homeLosses"]}-{team_data["homeOtLosses"]}".center(10),
            Away            = f"{team_data["roadWins"]}-{team_data["roadLosses"]}-{team_data["roadOtLosses"]}".center(10),
            Streak          = f"{team_data["streakCode"]}{team_data["streakCount"]}".center(8)
        )

    BORDER              : str = "+=====+=========================+====+===+===+====+=====+======+==========+==========+========+"
    INFO                : str = "|Pos. | Team                    | GP | W | L | OT | PTS | DIFF |   HOME   |   AWAY   | STREAK |"

    LEAGUE_HEADER       : str = "|                                    NATIONAL HOCKEY LEAGUE                                   |"

    EASTERN_HEADER      : str = "|                                           EASTERN                                           |"
    WESTERN_HEADER      : str = "|                                           WESTERN                                           |"

    ATLANTIC_HEADER     : str = "|                                           ATLANTIC                                          |"
    METROPOLITAN_HEADER : str = "|                                         METROPOLITAN                                        |"
    CENTRAL_HEADER      : str = "|                                           CENTRAL                                           |"
    PACIFIC_HOLDER      : str = "|                                           PACIFIC                                           |"

    ReleventData : list[dict] = data["standings"]
    FilterType : str = args.type

    if FilterType == "division":

        AtlanticHolder      : str = f"{ATLANTIC_HEADER}\n{BORDER}\n{INFO}\n{BORDER}\n"
        MetropolitanHolder  : str = f"{METROPOLITAN_HEADER}\n{BORDER}\n{INFO}\n{BORDER}\n"
        CentralHolder       : str = f"{CENTRAL_HEADER}\n{BORDER}\n{INFO}\n{BORDER}\n"
        PacificHolder       : str = f"{PACIFIC_HOLDER}\n{BORDER}\n{INFO}\n{BORDER}\n"

        for team_data in ReleventData:
            Row : str = formatTeamRow(team_data, "divisionSequence")

            Division = team_data["divisionAbbrev"]

            if Division == "A":
                AtlanticHolder += Row
            elif Division == "M":
                MetropolitanHolder += Row
            elif Division == "C":
                CentralHolder += Row
            elif Division == "P":
                PacificHolder += Row

        return f"{BORDER}\n{AtlanticHolder}{BORDER}\n{MetropolitanHolder}{BORDER}\n{CentralHolder}{BORDER}\n{PacificHolder}{BORDER}"

    elif FilterType == "conference":

        EasternHolder = f"{EASTERN_HEADER}\n{BORDER}\n{INFO}\n{BORDER}\n"
        WesternHolder = f"{WESTERN_HEADER}\n{BORDER}\n{INFO}\n{BORDER}\n"

        for team_data in ReleventData:
            Row : str = formatTeamRow(team_data, "conferenceSequence")

            Conference = team_data["conferenceAbbrev"]

            if Conference == "E":
                EasternHolder += Row
            elif Conference == "W":
                WesternHolder += Row

        return f"{BORDER}\n{EasternHolder}{BORDER}\n{WesternHolder}{BORDER}"

    else:

        LeagueHolder : str = f"{BORDER}\n{LEAGUE_HEADER}\n{BORDER}\n{INFO}\n{BORDER}\n"

        for team_data in ReleventData:
            LeagueHolder += formatTeamRow(team_data)

        return f"{LeagueHolder}{BORDER}"

def _formatScores(data : dict, args) -> str:
    """
    Formats scores data

    data : dict
        Scores data. See sameples/scores.json for structure reference

    args : argparse.Namespace
        

    return str
        Formatted scores output
    """

    ReleventData : list[dict] = data["games"]
    NumberOfGames : int = len(ReleventData) - 1

    # FilterType : str = args.type

    Output : list[str] = []
    GameIndex : int = 0
    while GameIndex <= NumberOfGames:

        print(GameIndex,NumberOfGames)
        GameL : dict = ReleventData[GameIndex]

        TimeL : str = datetime.strptime(GameL["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%SUTC")

        HomeTeamL : str = GameL["homeTeam"]["name"]["default"].ljust(24)
        HomeScoreL : str = str(GameL["homeTeam"].get("score","N/A")).center(3)

        AwayTeamL : str = GameL["awayTeam"]["name"]["default"].ljust(24)
        AwayScoreL : str = str(GameL["awayTeam"].get("score","N/A")).center(3)

        if (GameIndex + 1) <= NumberOfGames:
            GameR : dict = ReleventData[GameIndex]

            TimeR = datetime.strptime(GameR["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%SUTC")

            HomeTeamR : str = GameR["homeTeam"]["name"]["default"].ljust(24)
            HomeScoreR : int = str(GameR["homeTeam"].get("score","N/A")).center(3)

            AwayTeamR : str = GameR["awayTeam"]["name"]["default"].ljust(24)
            AwayScoreR : int = str(GameR["awayTeam"].get("score","N/A")).center(3)

            Output.append(f"{TimeL}                                        {TimeR}")
            Output.append(f"{HomeTeamL}||{HomeScoreL}||                               {HomeTeamR}||{HomeScoreR}||")
            Output.append(f"{AwayTeamL}||{AwayScoreL}||                               {AwayTeamR}||{AwayScoreR}||\n")

        else:
            Output.append(f"{TimeL}")
            Output.append(f"{HomeTeamL}||{HomeScoreL}||")
            Output.append(f"{AwayTeamL}||{AwayScoreL}||\n")

        GameIndex += 2

    return "\n".join(Output)





FormatMapping : dict[str, callable] = {
    "standings" : _formatStandings,
    "scores" : _formatScores,
}

def renderOutput(arguments, data : dict) -> None:
    """
    Formats and outputs the data onto the terminal

    arguments : argparse.Namespace
        Given user arguements

    data : dict
        Response data
    """

    if isinstance(data, str):
        print(data)
        return

    Render : str = FormatMapping[arguments.data](data, arguments.type)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(Render)