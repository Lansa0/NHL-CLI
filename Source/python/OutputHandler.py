import os

def _formatStandings(data : dict, data_type : str | None) -> str:
    """
    Formats the standings data

    data : dict
        Standings data

    return str
        Formatted output
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


    ReleventData = data["standings"]

    BORDER              : str = "+=====+=========================+====+===+===+====+=====+======+==========+==========+========+"
    INFO                : str = "|Pos. | Team                    | GP | W | L | OT | PTS | DIFF |   HOME   |   AWAY   | STREAK |"

    LEAGUE_HEADER       : str = "|                                    NATIONAL HOCKEY LEAGUE                                   |"

    EASTERN_HEADER      : str = "|                                           EASTERN                                           |"
    WESTERN_HEADER      : str = "|                                           WESTERN                                           |"

    ATLANTIC_HEADER     : str = "|                                           ATLANTIC                                          |"
    METROPOLITAN_HEADER : str = "|                                         METROPOLITAN                                        |"
    CENTRAL_HEADER      : str = "|                                           CENTRAL                                           |"
    PACIFIC_HOLDER      : str = "|                                           PACIFIC                                           |"

    if data_type == "division":

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

    elif data_type == "conference":

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


FormatMapping : dict[str, callable] = {
    "standings" : _formatStandings
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