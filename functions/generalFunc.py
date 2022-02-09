import nextcord

def Ranking2Embeds(ranking,fTitle,description,header,color):
  res = []
  fieldsLimit = 25
  totalLimit = 6000
  fieldsCur = 0
  totalCur = len(header)
  fname = header
  rEmbed = nextcord.Embed(
    title = fTitle,
    description = description,
    color = color
  )
  totalCur = len(rEmbed.title) + len(rEmbed.description)
  for mes in ranking:
    if fieldsCur+1 >= fieldsLimit or totalCur + len(mes) + 256 >= totalLimit:
      res.append(rEmbed)
      rEmbed = nextcord.Embed(
        description = description,
        color = color
      )
      rEmbed.add_field(name=header,value=mes,inline=False)
      totalCur = len(description) + totalCur + len(header)
    else:
      if fname == '':
        fname = mes
        totalCur += len(mes)
        continue
      rEmbed.add_field(name=fname,value=mes,inline=False)
      fname = ''
    fieldsCur +=1
    totalCur += len(mes)
  if fname != '':
    rEmbed.add_field(name=fname,value='°_°',inline=False)
  res.append(rEmbed)
  return res