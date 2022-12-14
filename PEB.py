from fpdf import FPDF


class PDF(FPDF):
    def create_table(self, table_data, title='', data_size=10, title_size=12, align_data='L', align_header='L',
                     cell_width='even', x_start='x_default', emphasize_data=[], emphasize_style=None,
                     emphasize_color=(0, 0, 0)):
        """
        table_data:
                    list of lists with first element being list of headers
        title:
                    (Optional) title of table (optional)
        data_size:
                    the font size of table data
        title_size:
                    the font size fo the title of the table
        align_data:
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header:
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width:
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start:
                    where the left edge of table should start
        emphasize_data:
                    which data elements are to be emphasized - pass as list
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black)

        """
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style

        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[
                                               0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])):  # for every row
                    longest = 0
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4)  # add 4 for padding
                col_width = col_widths

                ### compare columns

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else:  # need to multiply cell width by number of cells to get table width
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2  # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)

        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height)  # move cursor back to the left margin

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for row in data:
                if x_start:  # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin

        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left, y3, x_right, y3)

print("Caso cometa algum erro enquanto preenche os dados, prossiga preenchendo as informa????es seguintes, pois ao fim de cada etapa ser?? poss??vel corrigir os dados incorretos")
print("Caso n??o queira preencher alguma informa????o, apenas digite - (h??fen) e prossiga.")
import numpy as np

data_as_dict = []
row = 5
col = 1
for x in range(0, row):
    data_as_dict.append([])

    for y in range(0, col):
        data_as_dict[x].append('R' + str(x) + 'C' + str(y))
data_as_dict[0][0] = "INFORMA????ES GERAIS DO PROJETO"
print("Preencha as informa????es gerais do projeto solicitadas")
print("T??tulo do projeto:")
texto = input()
data_as_dict[1][0] = "T??tulo do projeto:" + texto

print("N??mero de refer??ncia do projeto:")
texto = input()
data_as_dict[2][0] = "N??mero de refer??ncia do projeto:" + texto

print("Breve descri????o do projeto:")
texto = input()
data_as_dict[3][0] = "Breve descri????o do projeto: " + texto

print("Localiza????o e endere??o do projeto:")
texto = input()
data_as_dict[4][0] = "Localiza????o e endere??o do projeto:" + texto
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a numera????o que deseja corrigir")
    print("1. T??tulo do Projeto")
    print("2. N??mero de refer??ncia do projeto")
    print("3. Breve Descri????o do projeto")
    print("4. Localiza????o e Endere??o do projeto")
    num2=int(input())
    print("Agora digite a informa????o correta:")
    if(num2==1):
      texto = input()
      data_as_dict[1][0] = "T??tulo do projeto:" + texto
    if(num2==2):
      texto = input()
      data_as_dict[2][0] = "N??mero de refer??ncia do projeto:" + texto
    if(num2==3):
      texto = input()
      data_as_dict[3][0] = "Breve descri????o do projeto: " + texto
    if(num2==4):
      texto = input()
      data_as_dict[4][0] = "Localiza????o e endere??o do projeto:" + texto
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
#-------------------------------------------------------------------------------------------------
print("MEMBROS DO PROJETO")
data = []
col = 6
x=0
data.append([])
for y in range(0, col):
    data[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data[0][0] = "Membro"
data[0][1] = "Nome"
data[0][2] = "Fun????o"
data[0][3] = "Empresa"
data[0][4] = "Email"
data[0][5] = "Telefone"

print("Digite as informa????es sobre cada membro do projeto um a um ")
data.append([])
for y in range(0, col):
  data[x].append('R' + str(x) + 'C' + str(y) )
texto1 = str(x)
data[x][0] = texto1
print("Membro", x)
print("Nome:")
texto2 = input()
data[x][1] = texto2
print("Fun????o:")
texto3 = input()
data[x][2] = texto3
print("Empresa:")
texto4 = input()
data[x][3] = texto4
print("Email:")
texto5 = input()
texto5 = str(texto5)
data[x][4] = texto5
print("Telefone:")
texto6 = input()
texto6 = str(texto6)
data[x][5] = texto6
t = 0
x=x+1
while (t == 0):
    print("Para continuar adicionando mais membros digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data.append([])
      for y in range(0, col):
        data[x].append('R' + str(x) + 'C' + str(y) )
      texto1 = str(x)
      data[x][0] = texto1
      print("Membro", x)
      print("Nome:")
      texto2 = input()
      data[x][1] = texto2
      print("Fun????o:")
      texto3 = input()
      data[x][2] = texto2
      print("Empresa:")
      texto4 = input()
      data[x][3] = texto4
      print("Email:")
      texto5 = input()
      texto5 = str(texto5)
      data[x][4] = texto5
      print("Telefone:")
      texto6 = input()
      texto6 = str(texto6)
      data[x][5] = texto6
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]])
for i in range (1,x):
  myTable.add_row([data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Nome")
    print("2. Fun????o")
    print("3. Empresa")
    print("4. Email")
    print("5. Telefone")
    num2=int(input())
    print("Agora digite a numera????o do membro cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Membro n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data[num3][1] = input()
      if(num2==2):
        data[num3][2] = input()
      if(num2==3):
        data[num3][3] = input()
      if(num2==4):
        data[num3][4] = input()
      if(num2==5):
        data[num3][5] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]])
    for i in range (1,x):
      myTable.add_row([data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]])
    print(myTable)
#-------------------------------------------------------------------------------------------------
data2 = []
print("Usos e Objetivos BIM")
print("Preencha as informa????es referentes aos objetivos e usos BIm.")
col = 4
x=0
data2.append([])
for y in range(0, col):
  data2[x].append('')
x=x+1
data2[0][0] = "Objetivo"
data2[0][1] = "Descri????o"
data2[0][2] = "N??vel de prioridade"
data2[0][3] = "Uso BIM relacionado"

plan = ["Capturar Condi????es Existentes", "Estimar Custo", "Modelo 3D", "Analisar requisitos do programa",
        "Analisar Crit??rios de Sele????o do Local", "Design Autoral", "Revisar Modelo(s) de Design"]
design = ["Analisar Desempenho Estrutural", "Analisar Desempenho da ilumina????o", "Analisar Desempenho Energ??tico",
          "Analisar Desempenho da Engenharia", "Analisar Desempenho da Sustentabilidade",
          "Coordenar Modelos de Design"]
constr = ["Modelo de Log??stica do Canteiro de Obras", "Modelo de Sistemas de Constru????o Tempor??ria",
          "Fabricar Produtos", "Layout do trabalho de constru????o"]
oper = ["Compilar modelo de registro", "Monitorar Manuten????o", "Monitorar o desempenho do sistema", "Monitorar ativos",
        "Monitorar a utiliza????o do espa??o", "Analisar Gerenciamento de Emerg??ncias"]
print("Digite abaixo o seu objetivo", x ,"BIM:")
data2.append([])
for y in range(0, col):
  data2[x].append('')
data2[x][0] = str(x)
data2[x][1] = input()
a=0
while(a==0):
  print("Qual ?? o n??vel de prioridade desse objetivo? (Digite a numera????o)")
  print("1. Alta")
  print("2. M??dia")
  print("3. Baixa")
  p = int(input())
  if p==1:
    print("Alta")
    data2[x][2] = "Alta"
    break
  if p==2:
    print("M??dia")
    data2[x][2] = "M??dia"
    break
  if p==3:
    print("Baixa")
    data2[x][2] = "Baixa"
    break
  if (p!=1 and p!=2 and p!=1):
    print("Op????o n??o existe. Tente novamente.")
x=x+1
t=0
while(t==0):
  print("Aperte 0 para encerrar ou 1 para adicionar mais um objetivo")
  n = int(input())
  if (n == 0):
    break
  if (n == 1):
    data2.append([])
    for y in range(0, col):
      data2[x].append('')
    print("Digite abaixo o objetivo", x,":")
    data2[x][0] = str(x)
    data2[x][1] = input()
    a=0
    while(a==0):
      print("Qual ?? o n??vel de prioridade desse objetivo? (Digite a numera????o)")
      print("1. Alta")
      print("2. M??dia")
      print("3. Baixa")
      p = int(input())
      if p==1:
        print("Alta")
        data2[x][2] = "Alta"
        x=x+1
        break
      if p==2:
        print("M??dia")
        data2[x][2] = "M??dia"
        x=x+1
        break
      if p==3:
        print("Baixa")
        data2[x][2] = "Baixa"
        x=x+1
        break
      if (p!=1 and p!=2 and p!=1):
        print("Op????o n??o existe. Tente novamente.")



print("Digite agora a numera????o dos usos BIM relacionados a cada objetivo:")
info=["Planejamento", "Design", "Constru????o", "Opera????o"]
t1 = ["1. Capturar Condi????es Existentes", "2. Estimar Custo", "3. Modelo 3D", "4. Analisar requisitos do programa",
        "5. Analisar Crit??rios de Sele????o do Local", "6. Design Autoral", "7. Revisar Modelo(s) de Design"]
t2 = ["8. Analisar Desempenho Estrutural", "9. Analisar Desempenho da ilumina????o", "10. Analisar Desempenho Energ??tico",
          "11. Analisar Desempenho da Engenharia", "12. Analisar Desempenho da Sustentabilidade",
          "13. Coordenar Modelos de Design", "-"]
t3 = ["14. Modelo de Log??stica do Canteiro de Obras", "15. Modelo de Sistemas de Constru????o Tempor??ria",
          "16. Fabricar Produtos", "17. Layout do trabalho de constru????o", "-", "-", "-"]
t4 = ["18. Compilar modelo de registro", "19. Monitorar Manuten????o", "20. Monitorar o desempenho do sistema", "21. Monitorar ativos",
        "22. Monitorar a utiliza????o do espa??o", "23. Analisar Gerenciamento de Emerg??ncias", "-"]
info=["Planejamento", "Design", "Constru????o", "Opera????o"]
from prettytable import PrettyTable
myTable= PrettyTable([info[0],info[1],info[2],info[3]])
for i in range (0,7):
  myTable.add_row([t1[i],t2[i],t3[i],t4[i]])
print(myTable)

for j in range(1, x):
    print("Digite o n??mero do uso BIM desejado para o seguinte objetivo:", data2[j][1],
          "Digite 0 quando quiser encerrar")
    k = 0
    while (k == 0):
        n = int(input())
        if (n == 0):
            print("Opera????o encerrada")
            break
        if (n == 1):
            print(plan[0])
            data2[j][3] = data2[j][3] + plan[0]
            data2[j][3] = data2[j][3] + '/'
        if (n == 2):
            print(plan[1])
            data2[j][3] = data2[j][3] + plan[1]
            data2[j][3] = data2[j][3] + '/'
        if (n == 3):
            print(plan[2])
            data2[j][3] = data2[j][3] + plan[2]
            data2[j][3] = data2[j][3] + '/'
        if (n == 4):
            print(plan[3])
            data2[j][3] = data2[j][3] + plan[3]
            data2[j][3] = data2[j][3] + '/'
        if (n == 5):
            print(plan[4])
            data2[j][3] = data2[j][3] + plan[4]
            data2[j][3] = data2[j][3] + '/'
        if (n == 6):
            print(plan[5])
            data2[j][3] = data2[j][3] + plan[1]
            data2[j][3] = data2[j][3] + '/'
        if (n == 7):
            print(plan[6])
            data2[j][3] = data2[j][3] + plan[1]
            data2[j][3] = data2[j][3] + '/'
        if (n == 8):
            print(design[0])
            data2[j][3] = data2[j][3] + design[0]
            data2[j][3] = data2[j][3] + '/'
        if (n == 9):
            print(design[1])
            data2[j][3] = data2[j][3] + design[1]
            data2[j][3] = data2[j][3] + '/'
        if (n == 10):
            print(design[2])
            data2[j][3] = data2[j][3] + design[2]
            data2[j][3] = data2[j][3] + '/'
        if (n == 11):
            print(design[3])
            data2[j][3] = data2[j][3] + design[3]
            data2[j][3] = data2[j][3] + '/'
        if (n == 12):
            print(design[4])
            data2[j][3] = data2[j][3] + design[4]
            data2[j][3] = data2[j][3] + '/'
        if (n == 13):
            print(design[5])
            data2[j][3] = data2[j][3] + design[5]
            data2[j][3] = data2[j][3] + '/'
        if (n == 14):
            print(constr[0])
            data2[j][3] = data2[j][3] + constr[0]
            data2[j][3] = data2[j][3] + '/'
        if (n == 15):
            print(constr[1])
            data2[j][3] = data2[j][3] + constr[1]
            data2[j][3] = data2[j][3] + '/'
        if (n == 16):
            print(constr[2])
            data2[j][3] = data2[j][3] + constr[2]
            data2[j][3] = data2[j][3] + '/'
        if (n == 17):
            print(constr[3])
            data2[j][3] = data2[j][3] + constr[3]
            data2[j][3] = data2[j][3] + '/'
        if (n == 18):
            print(oper[0])
            data2[j][3] = data2[j][3] + oper[0]
            data2[j][3] = data2[j][3] + '/'
        if (n == 19):
            print(oper[1])
            data2[j][3] = data2[j][3] + oper[1]
            data2[j][3] = data2[j][3] + '/'
        if (n == 20):
            print(oper[2])
            data2[j][3] = data2[j][3] + oper[2]
            data2[j][3] = data2[j][3] + '/'
        if (n == 21):
            print(oper[3])
            data2[j][3] = data2[j][3] + oper[3]
            data2[j][3] = data2[j][3] + '/'
        if (n == 22):
            print(oper[4])
            data2[j][3] = data2[j][3] + oper[4]
            data2[j][3] = data2[j][3] + '/'
        if (n == 23):
            print(oper[5])
            data2[j][3] = data2[j][3] + oper[5]
            data2[j][3] = data2[j][3] + '/'
        print("Se quiser continuar adicionando usos Bim relacionados ao seu objetivo, digite 1. Caso contr??rio, digite 0.")
        aux = int(input())
        if (aux == 0):
            break
        if (aux == 1):
            print("Digite o n??mero do pr??ximo Uso BIM:")



nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data2[0][0],data2[0][1],data2[0][2],data2[0][3]])
for i in range (1,x):
  myTable.add_row([data2[i][0],data2[i][1],data2[i][2],data2[i][3]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Descri????o")
    print("2. N??vel de prioridade")
    print("3. Uso BIM relacionado")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:

      if(num2==1):
        print("Digite a descri????o do objetivo correta:")
        data2[num3][1] = input()
      if(num2==2):
        while(a==0):
          print("Qual ?? o n??vel de prioridade correto desse objetivo? (Digite a numera????o)")
          print("1. Alta")
          print("2. M??dia")
          print("3. Baixa")
          p = int(input())
          if p==1:
            print("Alta")
            data2[num3][2] = "Alta"
            break
          if p==2:
            print("M??dia")
            data2[num3][2] = "M??dia"
            break
          if p==3:
            print("Baixa")
            data2[num3][2] = "Baixa"
            break
          if (p!=1 and p!=2 and p!=1):
            print("Op????o n??o existe. Tente novamente.")
      if(num2==3):
        k = 0
        data2[num3][3] =""
        print("Digite o n??mero do uso BIM correto para o objetivo:", data2[num3][1],
          "Digite 0 quando quiser encerrar")
        while (k == 0):
          myTable= PrettyTable([info[0],info[1],info[2],info[3]])
          for i in range (0,7):
            myTable.add_row([t1[i],t2[i],t3[i],t4[i]])
          print(myTable)
          n = int(input())
          if (n == 0):
            print("Opera????o encerrada")
            break
          if (n == 1):
            print(plan[0])
            data2[num3][3] = data2[num3][3] + plan[0]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 2):
            print(plan[1])
            data2[num3][3] = data2[num3][3] + plan[1]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 3):
            print(plan[2])
            data2[num3][3] = data2[num3][3] + plan[2]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 4):
            print(plan[3])
            data2[num3][3] = data2[num3][3] + plan[3]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 5):
            print(plan[4])
            data2[num3][3] = data2[num3][3] + plan[4]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 6):
            print(plan[5])
            data2[num3][3] = data2[num3][3] + plan[1]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 7):
            print(plan[6])
            data2[num3][3] = data2[num3][3] + plan[1]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 8):
            print(design[0])
            data2[num3][3] = data2[num3][3] + design[0]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 9):
            print(design[1])
            data2[num3][3] = data2[num3][3] + design[1]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 10):
            print(design[2])
            data2[num3][3] = data2[num3][3] + design[2]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 11):
            print(design[3])
            data2[num3][3] = data2[num3][3] + design[3]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 12):
            print(design[4])
            data2[num3][3] = data2[num3][3] + design[4]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 13):
            print(design[5])
            data2[num3][3] = data2[num3][3] + design[5]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 14):
            print(constr[0])
            data2[num3][3] = data2[num3][3] + constr[0]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 15):
            print(constr[1])
            data2[num3][3] = data2[num3][3] + constr[1]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 16):
            print(constr[2])
            data2[num3][3] = data2[num3][3] + constr[2]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 17):
            print(constr[3])
            data2[num3][3] = data2[num3][3] + constr[3]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 18):
            print(oper[0])
            data2[num3][3] = data2[num3][3] + oper[0]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 19):
            print(oper[1])
            data2[num3][3] = data2[num3][3] + oper[1]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 20):
            print(oper[2])
            data2[num3][3] = data2[num3][3] + oper[2]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 21):
            print(oper[3])
            data2[num3][3] = data2[num3][3] + oper[3]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 22):
            print(oper[4])
            data2[num3][3] = data2[num3][3] + oper[4]
            data2[num3][3] = data2[num3][3] + '/'
          if (n == 23):
            print(oper[5])
            data2[num3][3] = data2[num3][3] + oper[5]
            data2[num3][3] = data2[num3][3] + '/'
          print("Se quiser continuar adicionando usos Bim relacionados ao seu objetivo, digite 1. Caso contr??rio, digite 0.")
          aux = int(input())
          if (aux == 0):
            break
          if (aux == 1):
            print("Digite o n??mero do pr??ximo Uso BIM relacionado:")

    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    myTable= PrettyTable([data2[0][0],data2[0][1],data2[0][2],data2[0][3]])
    for i in range (1,x):
      myTable.add_row([data2[i][0],data2[i][1],data2[i][2],data2[i][3]])
    print(myTable)
    num1=int(input())
    if(num1==0):
      break

#-------------------------------------------------------------------------------------------------
print("CRONOGRAMA DO PROJETO")
data4 = []

col = 5

x=0
data4.append([])
for y in range(0, col):
  data4[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data4[0][0] = " "
data4[0][1] = "Fase do projeto"
data4[0][2] = "Data estimada de in??cio"
data4[0][3] = "Data estimada de fim"
data4[0][4] = "Partes envolvidas no projeto"
print("Digite as fases do seu projeto e as informa????es que s??o pedidas referentes a cada fase.")
data4.append([])
for y in range(0, col):
  data4[x].append('R' + str(x) + 'C' + str(y) )
data4[1][0]= str(x)
print("Fase do projeto:")
data4[1][1] = input()
print("Data estimada de in??cio:")
data4[1][2] = input()
print("Data estimada de fim")
data4[1][3]= input()
print("Partes envolvidas no projeto:")
data4[1][4]= input()
x=x+1
t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais fases digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data4.append([])
      for y in range(0, col):
        data4[x].append('R' + str(x) + 'C' + str(y) )
      data4[x][0] = str(x)
      print("Fase do projeto:")
      data4[x][1] = input()
      print("Data estimada de in??cio:")
      data4[x][2] = input()
      print("Data estimada de fim")
      data4[x][3]= input()
      print("Partes envolvidas no projeto:")
      data4[x][4]= input()
      x=x+1
    if f==0:
      break

nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data4[0][0],data4[0][1],data4[0][2],data4[0][3], data4[0][4]])
for i in range (1,x):
  myTable.add_row([data4[i][0],data4[i][1],data4[i][2],data4[i][3], data4[i][4]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Fase do projeto")
    print("2. Data estimada de in??cio")
    print("3. Data estimada de fim")
    print("4. Partes envolvidas no projeto")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data4[num3][1] = input()
      if(num2==2):
        data4[num3][2] = input()
      if(num2==3):
        data4[num3][3] = input()
      if(num2==4):
        data4[num3][4] = input()
      if(num2==5):
        data4[num3][5] = input()
      if(num2==6):
        data4[num3][6] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data4[0][0],data4[0][1],data4[0][2],data4[0][3], data4[0][4]])
    for i in range (1,x):
      myTable.add_row([data4[i][0],data4[i][1],data4[i][2],data4[i][3], data4[i][4]])
    print(myTable)
#-------------------------------------------------------------------------------------------------
print("FUN????ES ORGANIZACIONAIS")
data5 = []

col = 5

x=0
data5.append([])
for y in range(0, col):
  data5[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data5[0][0] = "Nome do modelo"
data5[0][1] = "Conte??do do modelo"
data5[0][2] = "Fase de projeto"
data5[0][3] = "Autor"
data5[0][4] = "Software e sua vers??o"
print("Digite o nome dos modelos e as informa????es que s??o pedidas referentes sobre cada um.")
data5.append([])
for y in range(0, col):
  data5[x].append('R' + str(x) + 'C' + str(y) )
x=x+1
print("Modelo 1")
print("Nome do modelo")
data5[1][0] = input()
print("Conte??do do modelo")
data5[1][1] = input()
print("Fase de projeto")
data5[1][2] = input()
print("Autor")
data5[1][3]= input()
print("Software e sua vers??o (Digite usando o seguinte formato : nome do software (vers??o). Separe os diferentes softwares por barras)")
data5[1][4]= input()
t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais modelos digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data5.append([])
      for y in range(0, col):
        data5[x].append('R' + str(x) + 'C' + str(y) )
      print("Modelo", x)
      print("Nome do modelo")
      data5[x][0] = input()
      print("Conte??do do modelo")
      data5[x][1] = input()
      print("Fase de projeto")
      data5[x][2] = input()
      print("Autor")
      data5[x][3]= input()
      print("Software e sua vers??o (Digite usando o seguinte formato : nome do software (vers??o). Separe os diferentes softwares por barras)")
      data5[x][4]= input()
      x=x+1
    if f==0:
      break

nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data5[0][0],data5[0][1],data5[0][2],data5[0][3], data5[0][4]])
for i in range (1,x):
  myTable.add_row([data5[i][0],data5[i][1],data5[i][2],data5[i][3], data5[i][4]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Nome do modelo")
    print("2. Conte??do do modelo")
    print("3. Fase do projeto")
    print("4. Autor")
    print("5. Software e sua vers??o")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data5[num3][0] = input()
      if(num2==2):
        data5[num3][1] = input()
      if(num2==3):
        data5[num3][2] = input()
      if(num2==4):
        data5[num3][3] = input()
      if(num2==5):
        data5[num3][4] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data5[0][0],data5[0][1],data5[0][2],data5[0][3], data5[0][4]])
    for i in range (1,x):
      myTable.add_row([data5[i][0],data5[i][1],data5[i][2],data5[i][3], data5[i][4]])
    print(myTable)

#----------------------------------------------------------------------------------------------------------------

data13= []
col = 7
x=0
data13.append([])
for y in range(0, col):
    data13[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data13[0][0] = " "
data13[0][1] = "Uso BIM"
data13[0][2] = "Organiza????o"
data13[0][3] = "N?? total de funcion??rios por uso BIM"
data13[0][4] = "Hor??rio estimado dos funcion??rios "
data13[0][5] = "Localiza????es"
data13[0][6] = "Contato principal"

print("Digite as informa????es solicitadas referentes aos Usos Bim e as pessoas envolvidas em cada uso: . ")
data13.append([])
for y in range(0, col):
  data13[x].append('R' + str(x) + 'C' + str(y) )
texto1 = str(x)
data13[x][0] = texto1
print("Uso BIM:")
texto2 = input()
data13[x][1] = texto2
print("Organiza????o:")
texto3 = input()
data13[x][2] = texto2
print("N??mero total de funcion??rios por uso BIM:")
texto4 = input()
data13[x][3] = texto4
print("Hor??rio estimado dos funcion??rios:")
texto4 = input()
texto4 = str(texto4)
data13[x][4] = texto4
print("Localiza????es:")
texto5 = input()
texto5 = str(texto5)
data13[x][5] = texto5
print("Contato principal:")
texto5 = input()
texto5 = str(texto5)
data13[x][6] = texto5
t = 0
x=x+1
while (t == 0):
    print("Para continuar adicionando mais Usos BIM e demais informa????es digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data13.append([])
      for y in range(0, col):
        data13[x].append('R' + str(x) + 'C' + str(y) )
      texto1 = str(x)
      data13[x][0] = texto1
      print("Uso BIM:")
      texto2 = input()
      data13[x][1] = texto2
      print("Organiza????o:")
      texto3 = input()
      data13[x][2] = texto2
      print("N??mero total de funcion??rios por uso BIM:")
      texto4 = input()
      data13[x][3] = texto4
      print("Hor??rio estimado dos funcion??rios:")
      texto4 = input()
      texto4 = str(texto4)
      data13[x][4] = texto4
      print("Localiza????es:")
      texto5 = input()
      texto5 = str(texto5)
      data13[x][5] = texto5
      print("Contato principal:")
      texto5 = input()
      texto5 = str(texto5)
      data13[x][6] = texto5
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data13[0][0],data13[0][1],data13[0][2],data13[0][3], data13[0][4],data13[0][5],data13[0][6]])
for i in range (1,x):
  myTable.add_row([data13[i][0],data13[i][1],data13[i][2],data13[i][3], data13[i][4],data13[i][5],data13[i][6]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Uso BIM")
    print("2. Organiza????o")
    print("3. N??mero total de funcion??rios por uso BIM")
    print("4. Hor??rio estimado dos funcion??rios")
    print("5. Localiza????es")
    print("6. Contato Principal")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data13[num3][1] = input()
      if(num2==2):
        data13[num3][2] = input()
      if(num2==3):
        data13[num3][3] = input()
      if(num2==4):
        data13[num3][4] = input()
      if(num2==5):
        data13[num3][5] = input()
      if(num2==6):
        data13[num3][6] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data13[0][0],data13[0][1],data13[0][2],data13[0][3], data13[0][4],data13[0][5],data13[0][6]])
    for i in range (1,x):
      myTable.add_row([data13[i][0],data13[i][1],data13[i][2],data13[i][3], data13[i][4],data13[i][5],data13[i][6]])
    print(myTable)
#--------------------------------------------------------------------------------------------------
print("NECESSIDADES DE INFRAESTRUTURA TECNOL??GICA - SOFTWARE")
data10= []
col = 5
x=0
data10.append([])
for y in range(0, col):
    data10[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data10[0][0] = " "
data10[0][1] = "Uso BIM"
data10[0][2] = "Disciplina (Se aplic??vel)"
data10[0][3] = "Software"
data10[0][4] = "Vers??o"


print("Digite as informa????es solicitadas sobre as necessidades de Infraestrutura tecnol??gica quanto a software")
data10.append([])
for y in range(0, col):
  data10[x].append('R' + str(x) + 'C' + str(y) )
texto1 = str(x)
data10[x][0] = texto1
print("Uso BIM:")
texto2 = input()
data10[x][1] = texto2
print("Disciplina (Se aplic??vel):")
texto3 = input()
data10[x][2] = texto2
print("Software:")
texto4 = input()
data10[x][3] = texto4
print("Vers??o:")
texto5 = input()
texto5 = str(texto5)
data10[x][4] = texto5
t = 0
x=x+1
while (t == 0):
    print("Para continuar adicionando mais Usos BIM e demais informa????es digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data10.append([])
      for y in range(0, col):
        data10[x].append('R' + str(x) + 'C' + str(y) )
      texto1 = str(x)
      data10[x][0] = texto1
      print("Uso BIM:")
      texto2 = input()
      data10[x][1] = texto2
      print("Disciplina (Se aplic??vel):")
      texto3 = input()
      data10[x][2] = texto2
      print("Software:")
      texto4 = input()
      data10[x][3] = texto4
      print("Vers??o:")
      texto5 = input()
      texto5 = str(texto5)
      data10[x][4] = texto5
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data10[0][0],data10[0][1],data10[0][2],data10[0][3], data10[0][4]])
for i in range (1,x):
  myTable.add_row([data10[i][0],data10[i][1],data10[i][2],data10[i][3], data10[i][4]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Uso BIM")
    print("2. Disciplina(Se aplic??vel)")
    print("3. Software")
    print("4. Vers??o")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data10[num3][1] = input()
      if(num2==2):
        data10[num3][2] = input()
      if(num2==3):
        data10[num3][3] = input()
      if(num2==4):
        data10[num3][4] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data10[0][0],data10[0][1],data10[0][2],data10[0][3],data10[0][4]])
    for i in range (1,x):
      myTable.add_row([data10[i][0],data10[i][1],data10[i][2],data10[i][3],data10[i][4]])
    print(myTable)
#-------------------------------------------------------------------------------------------------
print("NECESSIDADES DE INFRAESTRUTURA TECNOL??GICA - HARDWARE/COMPUTADORES")
data11= []
col = 5
x=0
data11.append([])
for y in range(0, col):
    data11[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data11[0][0] = " "
data11[0][1] = "Uso BIM"
data11[0][2] = "Hardware"
data11[0][3] = "Propriet??rio do Hardware"
data11[0][4] = "Especifica????es"


print("Digite as informa????es solicitadas sobre as necessidades de Infraestrutura tecnologica quanto ao hardware")
data11.append([])
for y in range(0, col):
  data11[x].append('R' + str(x) + 'C' + str(y) )
texto1 = str(x)
data11[x][0] = texto1
print("Uso BIM:")
texto2 = input()
data11[x][1] = texto2
print("Hardware:")
texto3 = input()
data11[x][2] = texto2
print("Propriet??rio do Hardware:")
texto4 = input()
data11[x][3] = texto4
print("Especifica????es:")
texto5 = input()
texto5 = str(texto5)
data11[x][4] = texto5
t = 0
x=x+1
while (t == 0):
    print("Para continuar adicionando mais Usos BIM e demais informa????es digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data11.append([])
      for y in range(0, col):
        data11[x].append('R' + str(x) + 'C' + str(y) )
      texto1 = str(x)
      data11[x][0] = texto1
      print("Uso BIM:")
      texto2 = input()
      data11[x][1] = texto2
      print("Hardware:")
      texto3 = input()
      data11[x][2] = texto2
      print("Propriet??rio do Hardware:")
      texto4 = input()
      data11[x][3] = texto4
      print("Especifica????es:")
      texto5 = input()
      texto5 = str(texto5)
      data11[x][4] = texto5
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data11[0][0],data11[0][1],data11[0][2],data11[0][3], data11[0][4]])
for i in range (1,x):
  myTable.add_row([data11[i][0],data11[i][1],data11[i][2],data11[i][3], data11[i][4]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Uso BIM")
    print("2. Hardware")
    print("3. Propriet??rio do Hardware")
    print("4. Especifica????es")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data11[num3][1] = input()
      if(num2==2):
        data11[num3][2] = input()
      if(num2==3):
        data11[num3][3] = input()
      if(num2==4):
        data11[num3][4] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data11[0][0],data11[0][1],data11[0][2],data11[0][3],data11[0][4]])
    for i in range (1,x):
      myTable.add_row([data11[i][0],data11[i][1],data11[i][2],data11[i][3],data11[i][4]])
    print(myTable)
#-------------------------------------------------------------------------------------------------
print("NECESSIDADES DE INFRAESTRUTURA TECNOL??GICA - CONTE??DO DE MODELAGEM E INFORMA????ES DE REFER??NCIA")
data12= []
col = 5
x=0
data12.append([])
for y in range(0, col):
    data12[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data12[0][0] = " "
data12[0][1] = "Uso BIM"
data12[0][2] = "Disciplina(Se aplic??vel)"
data12[0][3] = "Conte??do de Modelagem e Inf. de Refer??ncia."
data12[0][4] = "Vers??o"


print("Digite as informa????es solicitadas sobre as necessidades de Infraestrutura tecnologica quanto ao conte??do de modelagem e informa????es de refer??nica. ")
data12.append([])
for y in range(0, col):
  data12[x].append('R' + str(x) + 'C' + str(y) )
texto1 = str(x)
data12[x][0] = texto1
print("Uso BIM:")
texto2 = input()
data12[x][1] = texto2
print("Disciplina(Se aplic??vel):")
texto3 = input()
data12[x][2] = texto2
print("Conte??do de Modelagem e Informa????es de Refer??ncia:")
texto4 = input()
data12[x][3] = texto4
print("Vers??o:")
texto5 = input()
texto5 = str(texto5)
data12[x][4] = texto5
t = 0
x=x+1
while (t == 0):
    print("Para continuar adicionando mais Usos BIM e demais informa????es digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data12.append([])
      for y in range(0, col):
        data12[x].append('R' + str(x) + 'C' + str(y) )
      texto1 = str(x)
      data12[x][0] = texto1
      print("Uso BIM:")
      texto2 = input()
      data12[x][1] = texto2
      print("Disciplina(Se aplic??vel):")
      texto3 = input()
      data12[x][2] = texto2
      print("Conte??do de Modelagem e Informa????es de Refer??ncia:")
      texto4 = input()
      data12[x][3] = texto4
      print("Vers??o:")
      texto5 = input()
      texto5 = str(texto5)
      data12[x][4] = texto5
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data12[0][0],data12[0][1],data12[0][2],data12[0][3], data12[0][4]])
for i in range (1,x):
  myTable.add_row([data12[i][0],data12[i][1],data12[i][2],data12[i][3], data12[i][4]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Uso BIM")
    print("2. Disciplina(Se aplic??vel)")
    print("3. Conte??do de Modelagem e Informa????es de Refer??ncia")
    print("4. Vers??o")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data12[num3][1] = input()
      if(num2==2):
        data12[num3][2] = input()
      if(num2==3):
        data12[num3][3] = input()
      if(num2==4):
        data12[num3][4] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data12[0][0],data12[0][1],data12[0][2],data12[0][3],data12[0][4]])
    for i in range (1,x):
      myTable.add_row([data12[i][0],data12[i][1],data12[i][2],data12[i][3],data12[i][4]])
    print(myTable)

#-------------------------------------------------------------------------------------------------
print("PROCEDIMENTOS DE COLABORA????O")
print("1. Estrat??gia de colabora????o")
data6 = []
print("Descreva a estrat??gia de colabora????o")
x=0
data6.append([])
data6[x].append('')
x=x+1
data6.append([])
data6[x].append('')
data6[0][0]="1. Estrat??gia de colabora????o"
data6[1][0] =  input()

nothing=0
print ("Deseja corrigir a Estrat??gia de Colabora????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data6[0][0]])
myTable.add_row([data6[1][0]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Digite a informa????o correta:")
    data6[1][0] = input()
    print("Deseja corrigir novamente?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data6[0][0]])
    myTable.add_row([data6[1][0]])
    print(myTable)
#-------------------------------------------------------------------------------------------------
print("2. Procedimentos de reuni??o")
print("Agora preencha as informa????es sobre os procedimentos de reuni??o")
data7 = []

col = 5

x=0
data7.append([])
for y in range(0, col):
  data7[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data7[0][0] = "Tipo de reuni??o"
data7[0][1] = "Fase de projeto"
data7[0][2] = "Frequ??ncia"
data7[0][3] = "Participantes"
data7[0][4] = "Localiza????o"
data7.append([])
for y in range(0, col):
  data7[x].append('R' + str(x) + 'C' + str(y) )
x=x+1
print("Tipo de reuni??o:")
data7[1][0] = input()
print("Fase de projeto:")
data7[1][1] = input()
print("Frequ??ncia:")
data7[1][2] = input()
print("Participantes:")
data7[1][3]= input()
print("Localiza????o:")
data7[1][4]= input()
t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais tipos de reuni??o digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data7.append([])
      for y in range(0, col):
        data7[x].append('R' + str(x) + 'C' + str(y) )
      print("Tipo de reuni??o:")
      data7[x][0] = input()
      print("Fase de projeto:")
      data7[x][1] = input()
      print("Frequ??ncia:")
      data7[x][2] = input()
      print("Participantes:")
      data7[x][3]= input()
      print("Localiza????o:")
      data7[x][4]= input()
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data7[0][0],data7[0][1],data7[0][2],data7[0][3], data7[0][4]])
for i in range (1,x):
  myTable.add_row([data7[i][0],data7[i][1],data7[i][2],data7[i][3], data7[i][4]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Tipo de reuni??o")
    print("2. Fase de projeto")
    print("3. Frequ??ncia")
    print("4. Participantes")
    print("5. Localiza????o")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data7[num3][1] = input()
      if(num2==2):
        data7[num3][2] = input()
      if(num2==3):
        data7[num3][3] = input()
      if(num2==4):
        data7[num3][4] = input()
      if(num2==5):
        data7[num3][5] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data7[0][0],data7[0][1],data7[0][2],data7[0][3],data7[0][4]])
    for i in range (1,x):
      myTable.add_row([data7[i][0],data7[i][1],data7[i][2],data7[i][3],data7[i][4]])
    print(myTable)
#-------------------------------------------------------------------------------------------------
print("3. Modelo de cronograma de entrega de troca de informa????es para submiss??o e aprova????o")
data9 = []
print("Preencha as informa????es solicitadas referente as trocas de informa????es para submiss??o e aprova????o")
data9 = []

col = 9

x=0
data9.append([])
for y in range(0, col):
  data9[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data9[0][0] = "Interc??mbio de informa????es"
data9[0][1] = "Remetente do arquivo"
data9[0][2] = "Destinat??rio do arquivo"
data9[0][3] = "Uma vez/Frequ??ncia"
data9[0][4] = "Data de vencimento/ Data de in??cio"
data9[0][5] = "Modelo de arquivo"
data9[0][6] = "Modelo de software"
data9[0][7] = "Tipo de arquivo original"
data9[0][8] = "Tipo de troca de arquivo"
data9.append([])
for y in range(0, col):
  data9[x].append('R' + str(x) + 'C' + str(y) )
x=x+1
print("Interc??mbio de informa????es:")
data9[1][0] = input()
print("Remetente do arquivo:")
data9[1][1] = input()
print("Destinat??rio do arquivo:")
data9[1][2] = input()
print("Uma vez/Frequ??ncia")
data9[1][3]= input()
print("Data de vencimento/ Data de in??cio")
data9[1][4]= input()
print("Modelo de arquivo")
data9[1][5]= input()
print("Modelo de software")
data9[1][6]= input()
print("Tipo de arquivo original")
data9[1][7]= input()
print("Tipo de troca de arquivo")
data9[1][8]= input()
t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais interc??mbios de informa????es digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data9.append([])
      for y in range(0, col):
        data9[x].append('R' + str(x) + 'C' + str(y) )
      print("Interc??mbio de informa????es:")
      data9[1][0] = input()
      print("Remetente do arquivo:")
      data9[1][1] = input()
      print("Destinat??rio do arquivo:")
      data9[1][2] = input()
      print("Uma vez/Frequ??ncia")
      data9[1][3]= input()
      print("Data de vencimento/ Data de in??cio")
      data9[1][4]= input()
      print("Modelo de arquivo")
      data9[1][5]= input()
      print("Modelo de software")
      data9[1][6]= input()
      print("Tipo de arquivo original")
      data9[1][7]= input()
      print("Tipo de troca de arquivo")
      data9[1][8]= input()
      x=x+1
    if f==0:
      break

#-------------------------------------------------------------------------------------------------
data14 = []
print("4. Espa??o de trabalho interativo")
print(" Descreva sobre os espa??os de trabalho no projeto. A equipe do projeto deve considerar o ambiente f??sico necess??rio ao longo do ciclo de vida do projeto para acomodar a colabora????o, comunica????o e revis??es necess??rias que melhorar??o o processo de tomada de decis??es. Descreva como a equipe do projeto ser?? localizada, considerando perguntas como ???a equipe ser?? alocada???? Em caso afirmativo, onde ?? a localiza????o e o que ser?? nesse espa??o? Haver?? um espa??o BIM? Se sim, onde estar?? localizado e o que estar?? nele, como computadores, projetores, mesas, configura????o de mesas? Inclua qualquer informa????o adicional necess??ria. ")
x=0
data14.append([])
data14[x].append('')
x=x+1
data14.append([])
data14[x].append('')
data14[0][0]="4. Espa??o de trabalho interativo"
data14[1][0] =  input()
#--------------------------------------------------------------------------------------------------
print ("5, Procedimentos de comunica????o eletr??nica")
data15= []
col = 7
x=0
data15.append([])
for y in range(0, col):
    data15[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data15[0][0] = " "
data15[0][1] = "Localiza????o do Arquivo"
data15[0][2] = "Estrutura do arquivo/nome"
data15[0][3] = "Tipo de arquivo"
data15[0][4] = "Proteger por senha "
data15[0][5] = "Mantenedor de arquivos"
data15[0][6] = "Atualizado"

print("Digite as informa????es solicitadas referentes aos Usos Bim e as pessoas envolvidas em cada uso: . ")
data15.append([])
for y in range(0, col):
  data15[x].append('R' + str(x) + 'C' + str(y) )
texto1 = str(x)
data15[x][0] = texto1
print("Localiza????o do Arquivo:")
texto2 = input()
data15[x][1] = texto2
print("Estrutura do arquivo/nome:")
texto3 = input()
data15[x][2] = texto2
print("Tipo de arquivo:")
texto4 = input()
data15[x][3] = texto4
print("Proteger por senha:")
texto4 = input()
texto4 = str(texto4)
data15[x][4] = texto4
print("Mantenedor de arquivos:")
texto5 = input()
texto5 = str(texto5)
data15[x][5] = texto5
print("Atualizado:")
texto5 = input()
texto5 = str(texto5)
data15[x][6] = texto5
t = 0
x=x+1
while (t == 0):
    print("Para continuar adicionando mais informa????es sobre os arquivos digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data15.append([])
      for y in range(0, col):
        data15[x].append('R' + str(x) + 'C' + str(y) )
      texto1 = str(x)
      data15[x][0] = texto1
      print("Localiza????o do Arquivo:")
      texto2 = input()
      data15[x][1] = texto2
      print("Estrutura do arquivo/nome:")
      texto3 = input()
      data15[x][2] = texto2
      print("Tipo de arquivo:")
      texto4 = input()
      data15[x][3] = texto4
      print("Proteger por senha:")
      texto4 = input()
      texto4 = str(texto4)
      data15[x][4] = texto4
      print("Mantenedor de arquivos:")
      texto5 = input()
      texto5 = str(texto5)
      data15[x][5] = texto5
      print("Atualizado:")
      texto5 = input()
      texto5 = str(texto5)
      data15[x][6] = texto5
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data15[0][0],data15[0][1],data15[0][2],data15[0][3], data15[0][4],data15[0][5],data15[0][6]])
for i in range (1,x):
  myTable.add_row([data15[i][0],data15[i][1],data15[i][2],data15[i][3], data15[i][4],data15[i][5],data15[i][6]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Localiza????o do Arquivo")
    print("2. Estrutura do arquivo/nome")
    print("3. Tipo de arquivo")
    print("4. Proteger por senha")
    print("5. Mantenedor de arquivos")
    print("6. Atualizado")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data15[num3][1] = input()
      if(num2==2):
        data15[num3][2] = input()
      if(num2==3):
        data15[num3][3] = input()
      if(num2==4):
        data15[num3][4] = input()
      if(num2==5):
        data15[num3][5] = input()
      if(num2==6):
        data15[num3][6] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data15[0][0],data15[0][1],data15[0][2],data15[0][3], data15[0][4],data15[0][5],data15[0][6]])
    for i in range (1,x):
      myTable.add_row([data15[i][0],data15[i][1],data15[i][2],data15[i][3], data15[i][4],data15[i][5],data15[i][6]])
    print(myTable)


#--------------------------------------------------------------------------------------------------
print("Controle de qualidade")
print("1. Estrat??gia para controle de qualidade")
print("Digite abaixo um checklist para controle de qualidade.")
data17 = []

col = 5

x=0
data17.append([])
for y in range(0, col):
  data17[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data17[0][0] = "Check"
data17[0][1] = "Defini????o "
data17[0][2] = "Parte respons??vel"
data17[0][3] = "Programa(s) de software"
data17[0][4] = "Frequ??ncia"
data17.append([])
for y in range(0, col):
  data17[x].append('R' + str(x) + 'C' + str(y) )
x=x+1
print("Check:")
data17[1][0] = input()
print("Defini????o:")
data17[1][1] = input()
print("Parte respons??vel:")
data17[1][2] = input()
print("Programa(s) de software:")
data17[1][3]= input()
print("Frequ??ncia:")
data17[1][4]= input()
t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais itens para o checklist digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data17.append([])
      for y in range(0, col):
        data17[x].append('R' + str(x) + 'C' + str(y) )
      print("Check:")
      data17[x][0] = input()
      print("Defini????o:")
      data17[x][1] = input()
      print("Parte respons??vel:")
      data17[x][2] = input()
      print("Programa(s) de software:")
      data17[x][3]= input()
      print("Frequ??ncia:")
      data17[x][4]= input()
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data17[0][0],data17[0][1],data17[0][2],data17[0][3], data17[0][4]])
for i in range (1,x):
  myTable.add_row([data17[i][0],data17[i][1],data17[i][2],data17[i][3], data17[i][4]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Check")
    print("2. Defini????o")
    print("3. Parte respons??vel")
    print("4. Programa(s) de software")
    print("5. Frequ??ncia")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data17[num3][0] = input()
      if(num2==2):
        data17[num3][1] = input()
      if(num2==3):
        data17[num3][2] = input()
      if(num2==4):
        data17[num3][3] = input()
      if(num2==5):
        data17[num3][4] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data17[0][0],data17[0][1],data17[0][2],data17[0][3],data17[0][4]])
    for i in range (1,x):
      myTable.add_row([data17[i][0],data17[i][1],data17[i][2],data17[i][3],data17[i][4]])
    print(myTable)
#--------------------------------------------------------------------------------------------------
print("2. Precis??o e toler??ncia do modelo")
print("Digite abaixo as informa????es referentes ??s toler??ncias dos modelos.")
data18 = []

col = 3

x=0
data18.append([])
for y in range(0, col):
  data18[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data18[0][0] = "Fase"
data18[0][1] = "Disciplina"
data18[0][2] = "Toler??ncia"

data18.append([])
for y in range(0, col):
  data18[x].append('R' + str(x) + 'C' + str(y) )
x=x+1
print("Fase:")
data18[1][0] = input()
print("Disciplina:")
data18[1][1] = input()
print("Toler??ncia:")
data18[1][2] = input()

t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais itens para o lista digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data18.append([])
      for y in range(0, col):
        data18[x].append('R' + str(x) + 'C' + str(y) )
      print("Fase:")
      data18[x][0] = input()
      print("Disciplina:")
      data18[x][1] = input()
      print("Toler??ncia:")
      data18[x][2] = input()
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data18[0][0],data18[0][1],data18[0][2]])
for i in range (1,x):
  myTable.add_row([data18[i][0],data18[i][1],data18[i][2]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. Fase")
    print("2. Disciplina")
    print("3. Toler??ncia")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data18[num3][0] = input()
      if(num2==2):
        data18[num3][1] = input()
      if(num2==3):
        data18[num3][2] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data18[0][0],data18[0][1],data18[0][2]])
    for i in range (1,x):
      myTable.add_row([data18[i][0],data18[i][1],data18[i][2]])
    print(myTable)

#--------------------------------------------------------------------------------------------------
print("ESTRUTURA DE NOMEA????O DE ARQUIVOS")
print("1. Estrutura do t??tulo de modelo")
print("Digite abaixo as informa????es referentes ?? estrutura de nomea????o para cada tipo de modelo.")
data19 = []

col = 2

x = 0
data19.append([])
for y in range(0, col):
    data19[x].append('R' + str(x) + 'C' + str(y))
x = x + 1
data19[0][0] = "Tipo de modelo"
data19[0][1] = "Estrutura do t??tulo"

data19.append([])
for y in range(0, col):
    data19[x].append('R' + str(x) + 'C' + str(y))
x = x + 1
print("Tipo de modelo:")
data19[1][0] = input()
print("Estrutura do t??tulo do modelo:")
data19[1][1] = input()

t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais itens para o lista digite 1 e para parar digite 0.")
    f = int(input())
    if f == 1:
        data19.append([])
        for y in range(0, col):
            data19[x].append('R' + str(x) + 'C' + str(y))
        print("Tipo de modelo:")
        data19[x][0] = input()
        print("Estrutura do t??tulo do modelo:")
        data19[x][1] = input()
        x = x + 1
    if f == 0:
        break
nothing = 0
print("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable

myTable = PrettyTable([data19[0][0], data19[0][1]])
for i in range(1, x):
    myTable.add_row([data19[i][0], data19[i][1]])
print(myTable)
num1 = int(input())
if (num1 == 1):
    while (nothing == 0):
        print("Selecione a informa????o que deseja corrigir")
        print("1. Tipo de modelo")
        print("2. Estrutura de t??tulo do modelo")
        num2 = int(input())
        print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
        num3 = int(input())
        if (num3 == 0 or num3 >= x):
            print("Linha n??o existe")
        else:
            print("Agora digite a informa????o correta:")
            if (num2 == 1):
                data19[num3][0] = input()
            if (num2 == 2):
                data19[num3][1] = input()
        print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
        num1 = int(input())
        if (num1 == 0):
            break
        myTable = PrettyTable([data19[0][0], data19[0][1]])
        for i in range(1, x):
            myTable.add_row([data19[i][0], data19[i][1]])
        print(myTable)
#--------------------------------------------------------------------------------------------------
print("2. Estrutura do modelo")
print("Digite abaixo as informa????es referentes ?? estrutura do modelo.")
data20 = []

col = 2

x=0
data20.append([])
for y in range(0, col):
  data20[x].append('R' + str(x) + 'C' + str(y))
x=x+1
data20[0][0] = "A modelagem deve evitar:"
data20[0][1] = "A modelagem deve:"


data20.append([])
for y in range(0, col):
  data20[x].append('R' + str(x) + 'C' + str(y) )
x=x+1
print("A modelagem deve evitar:")
data20[1][0] = input()
print("A modelagem deve:")
data20[1][1] = input()


t = 0
i = 1
while (t == 0):
    print("Para continuar adicionando mais itens para o lista digite 1 e para parar digite 0.")
    f=int(input())
    if f==1:
      data20.append([])
      for y in range(0, col):
        data20[x].append('R' + str(x) + 'C' + str(y) )
      print("A modelagem deve evitar:")
      data20[x][0] = input()
      print("A modelagem deve:")
      data20[x][1] = input()
      x=x+1
    if f==0:
      break
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data20[0][0],data20[0][1]])
for i in range (1,x):
  myTable.add_row([data20[i][0],data20[i][1]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Selecione a informa????o que deseja corrigir")
    print("1. O modelo deve evitar")
    print("2. O modelo deve")
    num2=int(input())
    print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>=x):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      if(num2==1):
        data20[num3][0] = input()
      if(num2==2):
        data20[num3][1] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data20[0][0],data20[0][1]])
    for i in range (1,x):
      myTable.add_row([data20[i][0],data20[i][1]])
    print(myTable)
#--------------------------------------------------------------------------------------------------
print("3. Exclus??es")
print("Digite abaixo as informa????es que devem ser exclu??das para cada modelo.")
data21 = []

col = 3

x = 0
data21.append([])
for y in range(0, col):
    data21[x].append('R' + str(x) + 'C' + str(y))
x = x + 1
data21[0][0] = " "
data21[0][1] = "Modelo"
data21[0][2] = "Itens a serem exclu??dos do modelo"

data21.append([])
for y in range(0, col):
    data21[x].append('R' + str(x) + 'C' + str(y))
x = x + 1
data21[1][0]= x-1
print("Tipo de modelo:")
data21[1][1] = input()
print("Item a ser exclu??do")
data21[1][2] = input()

a=1

t = 0
j=0
i = 1
while (t == 0):
  while(j==0):
    print("Para continuar adicionando mais itens a serem exclu??dos para ", data21[a][0], "digite 1 e para parar digite 0.")
    f = int(input())
    if f == 1:
        data21.append([])
        for y in range(0, col):
            data21[x].append('R' + str(x) + 'C' + str(y))
        print("Item a ser exclu??do do modelo:")
        data21[x][0]= x
        data21[x][1] = " "
        data21[x][2] = input()
        x = x + 1
    if f == 0:
        break
  print("Para adicionar um novo tipo de modelo e itens a serem exclu??dos dele, digite 1 e para parar digite 0.")
  f = int(input())
  if f == 1:
    data21.append([])
    for y in range(0, col):
      data21[x].append('R' + str(x) + 'C' + str(y))
    data21[x][0]= x
    print("Tipo de modelo:")
    data21[x][1] = input()
    a=x
    print("Item a ser exclu??do do modelo:")
    data21[x][2] = input()
    x = x + 1
  if f == 0:
    break
nothing = 0
print("Deseja corrigir alguma informa????o? (Digite 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable

myTable = PrettyTable([data21[0][0], data21[0][1], data21[0][2]])
for i in range(1, x):
    myTable.add_row([data21[0][0], data21[0][1], data21[0][2]])
print(myTable)
num1 = int(input())
if (num1 == 1):
    while (nothing == 0):
        print("Selecione a informa????o que deseja corrigir")
        print("1. Tipo de modelo")
        print("2. Item a ser exclu??do do modelo")
        num2 = int(input())
        print("Agora digite a numera????o da linha cuja informa????o quer alterar:")
        num3 = int(input())
        if (num3 == 0 or num3 >= x):
            print("Linha n??o existe")
        else:
            print("Agora digite a informa????o correta:")
            if (num2 == 1):
                data21[num3][1] = input()
            if (num2 == 2):
                data21[num3][2] = input()
        print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
        myTable = PrettyTable([data21[0][0], data21[0][1], data21[0][2]])
        for i in range(1, x):
          myTable.add_row([data21[0][0], data21[0][1], data21[0][2]])
        print(myTable)

        num1 = int(input())
        if (num1 == 0):
            break


#--------------------------------------------------------------------------------------------------
print("4. Categoria de objetos REVIT")
print("Digite abaixo as informa????es referentes ?? categoria de objetos REVIT")
data22 = []
col = 2
x=0
data22.append([])
while(x<=36):
  for y in range(0, col):
    data22[x].append('R' + str(x) + 'C' + str(y))
  x=x+1
  data22.append([])


data22[0][0] = "Categoria de objeto"
data22[0][1] = "Status"
data22[1][0] = "??rea"
data22[2][0] = "M??veis sob encomenda"
data22[3][0] = "Tetos"
data22[4][0] = "Colunas"
data22[5][0] = "Cortina de vidro"
data22[6][0] = "Itens de detalhe"
data22[7][0] = "Portas"
data22[8][0] = "Equipamento el??trico"
data22[9][0] = "Instala????es el??tricas"
data22[10][0] = "Entorno"
data22[11][0] = "Pisos"
data22[12][0] = "M??veis/sistemas"
data22[13][0] = "Modelos gen??ricos "
data22[14][0] = "Ilumina????o"
data22[15][0] = "Linhas"
data22[16][0] = "Massa"
data22[17][0] = "Equipamento Mec??nico"
data22[18][0] = "Estacionamento"
data22[19][0] = "Vegeta????o"
data22[20][0] = "Encanamento"
data22[21][0] = "Guarda corpo"
data22[22][0] = "Rampas"
data22[23][0] = "Imagens rasterizadas"
data22[24][0] = "Estradas"
data22[25][0] = "Telhados"
data22[26][0] = "Espa??os"
data22[27][0] = "Shafts"
data22[28][0] = "Local"
data22[29][0] = "Equipamento especial"
data22[30][0] = "Vigas"
data22[31][0] = "Pilares"
data22[32][0] = "Projeto de funda????es"
data22[33][0] = "Projeto a??o estrutural "
data22[34][0] = "Topografia"
data22[35][0] = "Paredes"
data22[36][0] = "Janelas"



for i in range (1, 37):
  print(data22[i][0])
  data22[i][1] = input()
  x=x+1

t = 0
i = 1
nothing=0
print ("Deseja corrigir alguma informa????o? (Digite o n??mero 1 se sim ou 0, caso contr??rio)")
from prettytable import PrettyTable
myTable= PrettyTable([data22[0][0],data22[0][1]])
for i in range (1,37):
  myTable.add_row([data22[i][0],data22[i][1]])
print(myTable)
num1=int(input())
if(num1==1):
  while(nothing==0):
    print("Digite a numera????o da linha cuja informa????o quer alterar:")
    num3=int(input())
    if( num3==0 or num3>36):
      print("Linha n??o existe")
    else:
      print("Agora digite a informa????o correta:")
      data22[num3][1] = input()
    print("Deseja trocar mais alguma informa????o?(Digite 1 se sim ou 0, caso contr??rio)")
    num1=int(input())
    if(num1==0):
      break
    myTable= PrettyTable([data22[0][0],data22[0][1]])
    for i in range (1,37):
      myTable.add_row([data22[i][0],data22[i][1]])
    print(myTable)
#--------------------------------------------------------------------------------------------------
pdf = PDF()
pdf.add_page()
pdf.set_font("Times", size=10)

pdf.create_table(table_data=data_as_dict,
                 title='                                                                            GUIA BIM - UFPE',
                 cell_width='even')
pdf.ln()

pdf.create_table(table_data=data, title='MEMBROS', cell_width='even')
pdf.ln()

pdf.create_table(table_data=data2, title='OBJETIVOS BIM', cell_width='even')
pdf.ln()

pdf.create_table(table_data=data4, title='FASES DO PROJETO', cell_width='even')
pdf.ln()

pdf.create_table(table_data=data5, title='FUN????ES ORGANIZACIONAIS', cell_width='even')
pdf.ln()
pdf.create_table(table_data=data13, title='', cell_width='even')
pdf.ln()
pdf.create_table(table_data=data10, title='NECESSIDADES DE INFRAESTRUTURA TECNOL??GICA - SOFTWARE', cell_width='even')
pdf.ln()
pdf.create_table(table_data=data11, title='NECESSIDADES DE INFRAESTRUTURA TECNOL??GICA - HARDWARE', cell_width='even')
pdf.ln()
pdf.create_table(table_data=data12, title='NECESSIDADES DE INFRAESTRUTURA TECNOL??GICA - CONTE??DO DE MODELAGEM E INFORMA????ES DE REFER??NCIA', cell_width='even')
pdf.ln()

pdf.create_table(table_data=data6, title='                                              PROCEDIMENTOS DE COLABORA????O  ', cell_width='even')
pdf.ln()

pdf.create_table(table_data=data7, title='2. Procedimentos de reuni??o', cell_width='even')
pdf.ln()
pdf.create_table(table_data=data9, title='3. Modelo de cronograma de entrega de troca de informa????es para submiss??o e aprova????o', cell_width='even')
pdf.create_table(table_data=data6, title='', cell_width='even')
pdf.ln()
pdf.create_table(table_data=data15, title='5. Procedimentos de comunica????o eletr??nica', cell_width='even')
pdf.ln()
pdf.create_table(table_data= data17, title= '                                                                CONTROLE DE QUALIDADE                                                                                                         1. Estrat??gia geral para controle de qualidade', cell_width='even')
pdf.ln()
pdf.create_table(table_data= data18, title= '                                                     2. Precis??o e toler??ncia do modelo', cell_width='even')
pdf.ln()
pdf.create_table(table_data= data19, title= '                                                     ESTRUTURA DO MODELO                                                                                                        1. Estrutura de nomea????o do t??tulo', cell_width='even')
pdf.ln()
pdf.create_table(table_data= data20, title= '                                                                  2. Padr??es de modelagem', cell_width='even')
pdf.ln()
pdf.create_table(table_data= data21, title= '                                                                  3. Exclus??es', cell_width='even')
pdf.ln()
pdf.create_table(table_data= data22, title= '                                                                  4. Categorias de objetos REVIT', cell_width='even')
pdf.ln()
pdf.output('guia_ufpe.pdf')
print("Opera????o encerrada")
