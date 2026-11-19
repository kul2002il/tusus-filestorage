#let year = [2026]

// Настройки страницы
#set page(
  paper: "a4",                          // 210 × 297 мм
  margin: (
    left: 30mm,                         // левое – 30 мм
    right: 15mm,                        // правое – 15 мм
    top: 20mm,                          // верхнее – 20 мм
    bottom: 20mm,                       // нижнее – 20 мм
  ),
  numbering: "1",                       // нумерация страниц
  number-align: center,
  footer: context {
    if counter(page).get().first() == 1 {
      align(center)[Томск #year]
    } else {
      align(center)[#counter(page).display("1")]
    }
  },
)

// Шрифт и текст
#let leading = 1.5em
#set text(
  font: ("Times New Roman", "Liberation Serif"),
  size: 14pt,
  lang: "ru",
  hyphenate: false,
)

// Отчистить стили
#show heading:        set text(font: ("Times New Roman", "Liberation Serif"), size: 14pt)
#show figure.caption: set text(font: ("Times New Roman", "Liberation Serif"), size: 14pt)
#show figure.caption: set par(leading: 1em)
#show table:          set text(font: ("Times New Roman", "Liberation Serif"), size: 14pt)
#show table:          set par(leading: 1em)
#show footnote:       set text(font: ("Times New Roman", "Liberation Serif"), size: 14pt)

#set par(
  justify: true,
  leading: leading,
  first-line-indent: (amount: 1.25cm, all: true),
)

// Списки: каждый элемент — обычный абзац с номером/маркером в начале


// Заголовки
#set heading(numbering: (..nums) => {
  let n = nums.pos()
  if n.len() == 1 {
    numbering("1", ..n)
  } else if n.len() == 2 {
    numbering("1.1", ..n)
  } else {
    numbering("1.1.1", ..n)
  }
})

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(1em)
  align(center, text(weight: "bold", it))
  v(1em)
}

#show heading.where(level: 2): it => {
  v(1em)
  align(center, text(weight: "bold", it))
  v(1em)
}

#let numberlessHeader(title) = {
  pagebreak(weak: true)
  heading(level: 1, numbering: none, title)
}

// Рисунки
#set figure(
  supplement: "Рисунок",
  numbering: (..nums) => {
    let n = nums.pos()
    let section = counter(heading.where(level: 1)).get().first()
    if n.len() >= 1 {
      numbering("1.1", section, n.at(0))
    } else {
      numbering("1", section)
    }
  },
)

#show figure.where(kind: image): set figure.caption(position: bottom)
#show figure.caption: set align(center)
#show figure.where(kind: image): set figure.caption(separator: [ – ])
#show figure.caption: set par(
  leading: 1em,
  first-line-indent: (amount: 0pt, all: true),
  justify: false,
)
#show figure.where(kind: image): it => {
  set align(center)
  set par(first-line-indent: 0pt)
  it
}

#show ref: it => {
  if it.element != none and it.element.func() == figure {
    link(it.target, {
      let full = it
      show it.element.caption.at("supplement").text: none
      full
    })
  } else {
    it
  }
}

// Подписи титульного листа

#let tileListExecutors(body) = {
  align(right, box(width: 6cm, {
    set par(first-line-indent: 0pt, justify: false)
    set align(left)
    body
  }))
}

#let titleCenter(body) = {
  set align(center)
  set par(first-line-indent: 0pt, justify: false)
  body
}

#let line(width) = {
  box(width: width, stroke: (bottom: 0.5pt))[ ]
}
#let signature = [
  #line(2cm)
]
#let date = [
  «#line(0.8cm)» #line(1.5cm) #year г.
]

// Концевые сноски
#let endnotes-state = state("endnotes", ())
#let endnote-counter = counter("endnote")

#let endnote(body) = {
  endnote-counter.step()
  context {
    let idx = endnote-counter.get().first()
    let source-label = label("endpoint-source:" + str(idx))
    let placement-label = label("endpoint-placement:" + str(idx))
    endnotes-state.update(x => x + ((idx, body, source-label, placement-label),))
    link(placement-label)[[#idx]] #source-label
  }
}

#let print-endnotes() = context {
  let notes = endnotes-state.get()
  if notes.len() == 0 { return }
  for (idx, body, source-label, placement-label) in notes {
    [
      #link(source-label)[#idx]. #body
      #placement-label
    ]
  }
  endnotes-state.update(())
}

// Приколы
#show "—": "–"
#let emptyLine = v(leading)




// Титульный лист


#titleCenter[
Министерство науки и высшего образования Российской Федерации

Федеральное государственное автономное образовательное
учреждение высшего образования

"Томский государственный университет систем управления и радиоэлектроники" (ТУСУР)

#emptyLine

Кафедра конструирования деталей и узлов радиоэлектронной аппаратуры (КУДР)

#emptyLine
]

#tileListExecutors[
«УТВЕРЖДАЮ»

Зав. каф. КУДР

#signature Артищев С.А.

#date
]

#emptyLine

#titleCenter[
ФУНКЦИОНАЛЬНЫЙ ГЕНЕРАТОР СИГНАЛОВ

Курсовая работа

по дисциплине

«Схемотехника электронных средств»
]

#emptyLine

#tileListExecutors[
Студент гр. 234-2

#signature И.В Кулманаков

#date

Руководитель

доктор техн. наук,

профессор каф. КУДР

#signature А.В. Филатов

#date
]

#pagebreak()



// ТЗ
#titleCenter[
Министерство науки и высшего образования Российской Федерации

Федеральное государственное автономное образовательное
учреждение высшего образования

"Томский государственный университет систем управления и радиоэлектроники" (ТУСУР)

#emptyLine

Кафедра конструирования деталей и узлов радиоэлектронной аппаратуры (КУДР)

#emptyLine

ЗАДАНИЕ

на курсовой проект по дисциплине «Схемотехника электронных средств»

Студенту группы 234-2, Кулманакову Илье Владимировичу
]

#let section-counter = counter("section")

#let increment(level) = {
  parbreak()
  section-counter.step(level: level)
  context section-counter.display("1.1.1")
  [.]
}
#let mark = [
  #parbreak()
  •
]

#increment(1) Тема проекта: Функциональный генератор импульсов
#increment(1) Срок сдачи работы на кафедру #date
#increment(1) Цель проекта: Овладеть расчётом и модельными исследованиями функционального генератора импульсов на операционных усилителях.
#increment(1) Исходные данные для проектирования:
#mark для прямоугольного сигнала регулировка скважности следования импульсов от 1,1 до 10;
#mark для треугольного сигнала регулировка отношение времени нарастания к периоду от 0,1 до 0,9;
#mark регулировка периода импульсов в пределах от 50 мкс до 0,5 с;
#mark регулировка амплитуды импульсов в пределах от 0В до 10В;
#mark регулировка постоянной составляющей выхода от -10В до 10В;
#mark нагрузка: активное сопротивление 1кОм.
#increment(1) Вопросы, подлежащие разработке:
#increment(2) Анализ известных схем генераторов по литературным источникам.
#increment(2) Выбор схемы генератора. Описание работы с применением временных диаграмм.
#increment(2) Расчёт элементов принципиальной схемы генератора.
#increment(2) Модельные экспериментальные исследования характеристик генератора с использованием прикладной программы.
#increment(1) Содержание пояснительной записки:
#increment(2) Титульный лист.
#increment(2) Лист задания с подписью преподавателя
#increment(2) Содержание
#increment(2) Введение
#increment(2) Анализ известных схем генераторов по литературным источникам.
#increment(2) Выбор схемы генератора. Описание работы с применением временных диаграмм.
#increment(2) Расчёт элементов принципиальной схемы генератора.
#increment(2) Экспериментальные исследования характеристик генератора.
#increment(2) Выводы по работе. Заключение.
#increment(1) Графический материал:
#increment(2) Принципиальная схема генератора.
#increment(2) Временные диаграммы работы генератора.
#increment(2) Характеристики генератора, временные эпюры, полученные с применением исследований на модели.

#emptyLine

#block(breakable: false, grid(
  columns: (10cm, 6cm),
  column-gutter: 0em,
  row-gutter: leading,
  [Дата выдачи задания], [#date],
  [Подпись руководителя], [#signature Филатов А.В.],
  [Подпись студента], [#signature Кулманаков И.В.],
))

#pagebreak()

// ---------- Содержание (можно опустить по примечанию 2) ----------
#outline(title: "СОДЕРЖАНИЕ", indent: auto)
#pagebreak()


#numberlessHeader[Введение]

Функциональный генератор является одним из базовых измерительных приборов в лаборатории радиоэлектроники, позволяющим формировать периодические сигналы различной формы – синусоидальной, прямоугольной и треугольной, которые необходимы для настройки и проверки аналоговых схем. В контексте учебного процесса ценность подобного прибора определяется не только его прикладными характеристиками, но и тем, насколько наглядно он демонстрирует принципы работы ключевых аналоговых узлов.

Коммерчески доступные наборы для сборки функциональных генераторов, как правило, строятся на специализированных интегральных микросхемах, например XR2206 или ICL8038. Такие решения обладают несомненными достоинствами — компактностью, воспроизводимостью, низкой стоимостью — однако они скрывают от учащегося внутреннюю структуру генератора, оставляя «чёрным ящиком» как формирователь сигнала, так и цепи его обработки. Студент, собирающий такой набор, осваивает монтаж и пайку, но не получает представления о том, каким образом операционный усилитель (ОУ) может выполнять функции генератора, интегратора, компаратора или усилителя.

Актуальность настоящей работы обусловлена необходимостью создания учебного стенда, который позволял бы студентам не просто использовать готовый прибор, но и проследить путь от принципиальной схемы до работающего устройства. Исходя из этого, в рамках данной курсовой работы ставится задача разработки функционального генератора сигналов, построенного исключительно на дискретных аналоговых компонентах — транзисторах и операционных усилителях — без применения специализированных интегральных генераторных микросхем. Каждый из узлов схемы допускает аналитическое описание, настройку и экспериментальную проверку, что делает его удобной дидактической единицей.

Таким образом, целью работы является разработка функционального генератора сигналов на аналоговых компонентах, пригодного для использования в качестве учебного набора для пайки.

= АНАЛИЗ ИМЕЮЩИХСЯ РЕШЕНИЙ
== Симметричная схема

#lorem(40)

== Схема с двумя диодами

Известна схема #endnote[Генераторы треугольных импульсов на ОУ | HomeElectronics URL: https://www.electronicsblog.ru/usilitelnaya-sxemotexnika/generatory-treugolnyx-impulsov-na-ou.html (дата обращения: 17.11.2016).]<ссылка_на_сайт_со_схемой>, представлена на рисунке@Схема_с_диодами.


#figure(
  image("Расчёты/img/схема с диодами в интеграторе.png"),
  caption: [Схема с диодами в цепи интегратора],
) <Схема_с_диодами>

= СИНТЕЗ СХЕМЫ

== Делаем раз

#lorem(40)

== Делаем два

#lorem(40)

= РАСЧЁТ ЭЛЕМЕНТОВ ПРИНЦИПИАЛЬНОЙ СХЕМЫ ГЕНЕРАТОРА

#lorem(40)

= ЭКСПЕРИМЕНТАЛЬНЫЕ ИССЛЕДОВАНИЯ ХАРАКТЕРИСТИК ГЕНЕРАТОРА

#lorem(40)

#numberlessHeader[Заключение]

#lorem(40)


#numberlessHeader[Список использованных источников]

#print-endnotes()
