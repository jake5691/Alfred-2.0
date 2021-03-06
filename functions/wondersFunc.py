from nextcord import Color

from functions.generalFunc import Ranking2Embeds
from functions.memberFunc import generate_table


def getWonderRankingEmbeds(memberList, wonderName, color:Color, above=1, progressSince=None):
  ranking = []
  for m in memberList:
    lvl, date_ = m.getWonderLvl(wonderName)
    if lvl == None or lvl == 0:
      continue
    r = [m.rName(), lvl, date_]
    ranking.append(r)
  #Sort Ranking
  ranking = sorted(ranking, key=lambda x: (1/x[1],x[2]), reverse=False)
  #Set standard values
  table = generate_table(ranking)
  title = f"{len(ranking)} of {len(memberList)} players {wonderName}."
  description = ""
  header = f"**Rank     Player                            {wonderName}**"
  embeds = Ranking2Embeds(table, title, description, header, color)
  return embeds