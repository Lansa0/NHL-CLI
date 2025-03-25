from datetime import datetime
import os

# TODO
# Put each row string in a list and join together, rather then adding to
# a new string

def _formatStandings(data : dict, args) -> str:
    """
    Formats standings data for output

    data -> dict
        Standings data. See samples/standings.json for structure reference

    args -> argparse.Namespace
        Given user input. Only using args.type from this to show what the 
        user wants to see.
        Valid type inputs:
        - division
        - conference
        - league (empty or non valid types defualt to this)

    return -> str
        Formatted standings output
    """

    Template_Row : str = "|{Position}| {Team}|{GP}|{Wins}|{Losses}|{Overtime}|{Points}|{Differential}|{Home}|{Away}|{Streak}|"
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

    Output : list[str] = []

    if FilterType == "division":

        DivisionRows : dict[str, list[str]] = {
            "A" : [f"{ATLANTIC_HEADER}\n{BORDER}\n{INFO}\n{BORDER}"],
            "M" : [f"{METROPOLITAN_HEADER}\n{BORDER}\n{INFO}\n{BORDER}"],
            "C" : [f"{CENTRAL_HEADER}\n{BORDER}\n{INFO}\n{BORDER}"],
            "P" : [f"{PACIFIC_HOLDER}\n{BORDER}\n{INFO}\n{BORDER}"]
        }

        for team_data in ReleventData:

            Row : str = formatTeamRow(team_data, "divisionSequence")
            Division : str = team_data["divisionAbbrev"]

            DivisionRows[Division].append(Row)

        Output +=  [
            BORDER,
            *DivisionRows["A"], BORDER,
            *DivisionRows["M"], BORDER,
            *DivisionRows["C"], BORDER,
            *DivisionRows["P"], BORDER
        ]

    elif FilterType == "conference":

        ConferenceRows : dict[str, list[str]] = {
            "E" : [f"{EASTERN_HEADER}\n{BORDER}\n{INFO}\n{BORDER}"],
            "W" : [f"{WESTERN_HEADER}\n{BORDER}\n{INFO}\n{BORDER}"]
        }

        for team_data in ReleventData:

            Row : str = formatTeamRow(team_data, "conferenceSequence")
            Conference : str = team_data["conferenceAbbrev"]

            ConferenceRows[Conference].append(Row)

        Output += [
            BORDER,
            *ConferenceRows["E"], BORDER,
            *ConferenceRows["W"], BORDER,
        ]

    else:

        Output.append(f"{BORDER}\n{LEAGUE_HEADER}\n{BORDER}\n{INFO}\n{BORDER}")

        for team_data in ReleventData:
            Output.append(formatTeamRow(team_data))

        Output.append(BORDER)

    return "\n".join(Output)

def _formatScores(data : dict, args) -> str:
    """
    Formats scores data

    data -> dict
        Scores data. See sameples/scores.json for structure reference

    args -> argparse.Namespace

    return -> str
        Formatted scores output
    """

    ReleventData : list[dict] = data["games"]
    NumberOfGames : int = len(ReleventData) - 1

    FilterType : str = args.type

    Output : list[str] = []
    GameIndex : int = 0
    while GameIndex <= NumberOfGames:

        GameL : dict = ReleventData[GameIndex]

        TimeL : str = datetime.strptime(GameL["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%SUTC")

        HomeTeamL : str = GameL["homeTeam"]["name"]["default"].ljust(25)
        HomeScoreL : str = str(GameL["homeTeam"].get("score","N/A")).center(3)

        AwayTeamL : str = GameL["awayTeam"]["name"]["default"].ljust(25)
        AwayScoreL : str = str(GameL["awayTeam"].get("score","N/A")).center(3)

        if (GameIndex + 1) <= NumberOfGames:
            GameR : dict = ReleventData[GameIndex + 1]

            TimeR = datetime.strptime(GameR["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%SUTC")

            HomeTeamR : str = GameR["homeTeam"]["name"]["default"].ljust(25)
            HomeScoreR : int = str(GameR["homeTeam"].get("score","N/A")).center(3)

            AwayTeamR : str = GameR["awayTeam"]["name"]["default"].ljust(25)
            AwayScoreR : int = str(GameR["awayTeam"].get("score","N/A")).center(3)

            Output.append(f"{TimeL}                                         {TimeR}")
            Output.append(f"{HomeTeamL}||{HomeScoreL}||                               {HomeTeamR}||{HomeScoreR}||")
            Output.append(f"{AwayTeamL}||{AwayScoreL}||                               {AwayTeamR}||{AwayScoreR}||")
            Output.append("")

        else:
            Output.append(f"{TimeL}")
            Output.append(f"{HomeTeamL}||{HomeScoreL}||")
            Output.append(f"{AwayTeamL}||{AwayScoreL}||")
            Output.append("")

        GameIndex += 2

    Output.pop()
    return "\n".join(Output)


FormatMapping : dict[str, callable] = {
    "standings" : _formatStandings,
    "scores" : _formatScores,
}

def renderOutput(arguments, data : dict) -> None:
    """
    Formats and outputs the data onto the terminal

    arguments -> argparse.Namespace
        Given user arguements

    data -> dict
        Response data
    """

    if isinstance(data, str):
        print(data)
        return

    Render : str = FormatMapping[arguments.data](data, arguments)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(Render)