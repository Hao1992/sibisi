# Menu data for Shibisi Ramen. Prices, names, allergens, intros, pairings.
# Allergen codes: G gluten, H egg, S soy, Sé sesame, M mushrooms (extra, not EU-14)

T = {
 "zh": dict(tagline="家常中餐 · Cocina china", eye="招牌菜", title="黄焖鸡米饭（砂锅）",
  desc="山东经典家常菜。鸡肉以酱油和香菇汁慢火焖煮，砂锅上桌，配青菜，含米饭。咸鲜下饭，默认不辣。",
  frm="套餐含米饭，起价",
  steps=["看到想吃的，点 ＋ 加进单子", "黄焖锅可以选辣度、加配菜；面里的香菜也可以不要", "选好点屏幕下方「查看我的单子」，把手机给店员看"],
  firstT="第一次来？推荐", take="外带请致电", copy="复制电话", copied="已复制",
  all="菌菇不属于欧盟规定的 14 类过敏原，我们额外标注。如有过敏，请告知店员。", algL="过敏原",
  veg="素食", vegan="纯素", extras="砂锅加配菜（另收费）", drinks="酒水",
  beers="啤酒", wine="葡萄酒", soft="饮料", water="水",
  promiseT="我们的坚持",
  promise=[["面", "我们的手工面，每一根都用小麦粉在店里制作（不是米粉）"], ["酱", "酱汁和汤底由店里按自家配方现调"], ["鲜", "手工面和黄焖锅不用预制，每一碗现点现做"]],
  more="查看详细介绍 ›", pairWith="可另点（另收费）：", orw="或", pairT="推荐加点（另收费，不含在主食里）", total="加点后合计",
  pairNote="以上小菜和饮料不含在主食价格里，需要另外点、另外付费。想加的话，点单时告诉店员菜号就行。", illo="示意图 · 实拍照片待补", close="关闭",
  by="菜单制作", by2="也能帮你的店做一份 ›",
  dirs="怎么走 ›", rev="在 Google 上给我们评价 ›",
  sayEs="西班牙语这么说", luckAgain="再选一个", today="今日", seeIt="看看这道 ›",
  slipT="吃完了？抽一张", slipSub="抽一张看看", scratch="手指刮开", slipOnce="刚抽过，等一分钟再抽下一张", slipAgain="再抽一张",
  chopT="不会用筷子？", chopEnd="拿不好也没关系，跟我们说一声就给你叉子。",
  hiAgain="又见面了 👋",
  packT="几个人吃？", packAdd="加进单子", packEach="人均 %s", packNote="先加上，再在单子里增减就行。",
  hrsT="营业时间", packSame="和单点同价，只是帮你把最搭的组合配好了",
  top="最多人点", fT="挑菜", fNoPork="不含猪肉", fNo="不辣", fWo="不含%s", fCount="%s 道菜", fClear="清除", fEmpty="没有同时满足这些条件的菜。少选一个条件试试，或者直接问店员。",
  adj="辣度：不辣、微辣、中辣、特辣（默认不辣）。加配菜另收费：土豆 +1,00 €，油菜 +1,20 €，白蘑菇 +1,60 €，金针菇 +1,60 €，米饭 +1,70 €。加辣用的辣椒油含芝麻。",
  pot="砂锅端上桌时还在咕嘟冒泡，这是黄焖锅最好吃的时刻。小心别碰锅边。先吃配菜，再把汤汁浇在米饭上拌着吃。"),
 "es": dict(tagline="Cocina china casera · 中餐", eye="Nuestro plato estrella", title="Estofado de pollo Huangmen",
  desc="Un clásico casero de Shandong, en el norte de China. Pollo cocinado a fuego lento en salsa de soja y setas, servido humeante en olla de barro, con verduras y arroz incluido. Salado y sabroso, sin picante si no lo pides.",
  frm="Menú con arroz, desde",
  steps=["¿Te apetece algo? Pulsa ＋ para añadirlo a tu lista", "En las ollas eliges el picante y puedes añadir extras; los fideos con cilantro, sin él", "Cuando acabes, abre «Ver mi pedido» abajo y enséñaselo al personal"],
  firstT="¿Primera vez? Te recomendamos", take="Para llevar, llámanos", copy="Copiar número", copied="Copiado",
  all="Las setas no están entre los 14 alérgenos obligatorios de la UE, pero las señalamos igualmente. Si tienes alguna alergia, avisa al personal.", algL="Alérgenos",
  veg="Vegetariano", vegan="Vegano", extras="Extras para tu olla (con suplemento)", drinks="Bebidas",
  beers="Cervezas", wine="Vino", soft="Refrescos", water="Agua",
  promiseT="Hecho aquí",
  promise=[["面", "Nuestros fideos caseros, hechos a mano en el local con harina de trigo (no son de arroz)"], ["酱", "Salsas y caldos preparados aquí con nuestra receta"], ["鲜", "Fideos caseros y ollas sin precocinados: cada plato se hace al momento"]],
  more="Ver detalles ›", pairWith="Para añadir (se paga aparte):", orw="o", pairT="Sugerencia para añadir (se paga aparte, no incluido)", total="Total si lo añades",
  pairNote="El entrante y la bebida no están incluidos en el precio del plato: se piden y se pagan aparte. Si los quieres, dile los números al personal.", illo="Ilustración · foto real próximamente", close="Cerrar",
  by="Carta hecha por", by2="También puedo hacer una para tu restaurante ›",
  dirs="Cómo llegar ›", rev="Déjanos una reseña en Google ›",
  sayEs="En español", luckAgain="Otra sugerencia", today="Hoy", seeIt="Ver el plato ›",
  slipT="¿Ya habéis acabado? Saca un papelito", slipSub="A ver qué te toca", scratch="Rasca con el dedo", slipOnce="Acabas de sacar uno: espera un minuto para el siguiente.", slipAgain="Sacar otro",
  chopT="¿No sabes usar los palillos?", chopEnd="Si no te salen, dínoslo y te traemos un tenedor.",
  hiAgain="¡Otra vez por aquí! 👋",
  packT="¿Cuántos sois?", packAdd="Añadir al pedido", packEach="%s por persona", packNote="Añádelo y luego ajusta lo que quieras en tu pedido.",
  hrsT="Horario", packSame="Mismo precio que pedirlo suelto: te ahorramos elegir, no el dinero",
  top="Los más pedidos", fT="Filtrar", fNoPork="Sin cerdo", fNo="Sin picante", fWo="Sin %s", fCount="%s platos", fClear="Quitar", fEmpty="No hay platos que cumplan todo esto. Prueba con un filtro menos, o pregúntanos.",
  adj="Nivel de picante: sin picante, suave, medio o muy picante (por defecto, sin picante). Extras con suplemento: patata +1,00 €, pak choi +1,20 €, champiñón +1,60 €, setas enoki +1,60 €, arroz +1,70 €. El aceite de chile que usamos para el picante lleva sésamo.",
  pot="La olla llega a la mesa todavía hirviendo: ese es el mejor momento. Cuidado, el borde quema. Empieza por los ingredientes y después echa la salsa sobre el arroz."),
 "en": dict(tagline="Home-style Chinese food · 中餐", eye="Our signature dish", title="Huangmen braised chicken pot",
  desc="A home-style classic from Shandong, northern China. Chicken slow-braised in soy and mushroom sauce, served bubbling in a clay pot with greens and rice included. Savoury, and not spicy unless you ask.",
  frm="Set with rice, from",
  steps=["See something you like? Tap ＋ to add it to your list", "Pots let you pick the spice level and add extras; noodles with coriander can come without", "When you are done, open “View my order” at the bottom and show it to our staff"],
  firstT="First time? Try these", take="Takeaway: call us", copy="Copy number", copied="Copied",
  all="Mushrooms aren't one of the EU's 14 mandatory allergens, but we mark them anyway. If you have an allergy, please tell our staff.", algL="Allergens",
  veg="Vegetarian", vegan="Vegan", extras="Pot extras (extra charge)", drinks="Drinks",
  beers="Beer", wine="Wine", soft="Soft drinks", water="Water",
  promiseT="Made here",
  promise=[["面", "Our handmade noodles are made in-house from wheat flour (not rice noodles)"], ["酱", "Sauces and broths mixed here to our own recipe"], ["鲜", "Our handmade noodles and pots are never pre-cooked: every bowl is made to order"]],
  more="See details ›", pairWith="Optional add-ons (extra charge):", orw="or", pairT="Suggested add-ons (extra charge, not included)", total="Total with add-ons",
  pairNote="Sides and drinks are not included in the dish price: they are ordered and paid separately. To add them, just tell our staff the numbers.", illo="Illustration · real photo coming soon", close="Close",
  by="Menu made by", by2="I can make one for your place too ›",
  dirs="Get directions ›", rev="Leave us a Google review ›",
  sayEs="In Spanish", luckAgain="Try another", today="Today", seeIt="See the dish ›",
  slipT="Finished? Draw a slip", slipSub="See what you get", scratch="Scratch with your finger", slipOnce="Just drawn — wait a minute for the next one.", slipAgain="Draw another",
  chopT="New to chopsticks?", chopEnd="If they are not working, just ask and we will bring you a fork.",
  hiAgain="Good to see you again 👋",
  packT="How many of you?", packAdd="Add to my order", packEach="%s per person", packNote="Add it, then adjust anything you like in your order.",
  hrsT="Opening hours", packSame="Same price as ordering separately — we just picked the combination for you",
  top="Most ordered", fT="Filter", fNoPork="No pork", fNo="Not spicy", fWo="No %s", fCount="%s dishes", fClear="Clear", fEmpty="No dishes match all of these. Try one filter fewer, or just ask us.",
  adj="Spice: none, mild, medium or extra hot (no spice by default). Extras at extra cost: potato +€1.00, pak choi +€1.20, button mushrooms +€1.60, enoki +€1.60, rice +€1.70. The chilli oil we use for spice contains sesame.",
  pot="The pot arrives still bubbling, which is the best moment to eat it. Careful, the rim is hot. Eat the toppings first, then spoon the sauce over your rice."),
}

LBL = {
 "zh": dict(what="这是什么", story="小故事", ing="主要食材", taste="口味与口感", adj="可以调整", how="怎么吃", note="需要知道", who="适合谁", alg="过敏原"),
 "es": dict(what="¿Qué es?", story="Un poco de historia", ing="Ingredientes principales", taste="Sabor y textura", adj="Puedes ajustar", how="Cómo se come", note="A tener en cuenta", who="Ideal para", alg="Alérgenos"),
 "en": dict(what="What it is", story="The story", ing="Main ingredients", taste="Taste & texture", adj="You can adjust", how="How to eat it", note="Good to know", who="Best for", alg="Allergens"),
}

ALGN = {"G": ["麸质", "Gluten", "Gluten"], "H": ["鸡蛋", "Huevo", "Egg"], "S": ["大豆", "Soja", "Soy"],
        "Sé": ["芝麻", "Sésamo", "Sesame"], "P": ["鱼类", "Pescado", "Fish"], "M": ["菌菇", "Setas", "Mushrooms"]}

TASTE = {
 "sabroso": ["咸鲜", "Salado y sabroso", "Savoury"], "suave": ["清淡", "Suave", "Mild"],
 "intenso": ["浓郁红烧", "Guisado intenso", "Rich & braised"], "acido": ["酸爽", "Ácido", "Tangy"],
 "agridulce": ["酸甜", "Agridulce", "Sweet & sour"], "picante": ["香辣", "Picante", "Spicy"],
 "mala": ["麻辣", "Picante mala", "Numbing-spicy"], "especias": ["香料味", "Especiado", "Aromatic spices"],
 "comino": ["孜然", "Comino", "Cumin"], "ajo": ["蒜香", "Ajo", "Garlicky"],
 "fresco": ["清爽", "Frío y fresco", "Cold & fresh"], "soja": ["酱香", "Salsa de soja", "Soy sauce"],
}

def d(c, zh, es, en, p, es2, en2, al, ta, fl="", img=None, p2=None):
    o = dict(c=c, zh=zh, es=es, en=en, p=p, es2=es2, en2=en2, al=al, ta=ta, fl=fl)
    if img: o["img"] = img
    if p2: o["p2"] = p2
    return o

S = [
 dict(id="hm", zh="黄焖套餐", es="Ollas Huangmen (con arroz)", en="Huangmen clay pots (with rice)",
  note=dict(zh="均含米饭，砂锅现煮。可选辣度，默认不辣。", es="Todas incluyen arroz. Se cocinan en olla de barro y salen hirviendo. Elige tu picante (por defecto, sin picante).", en="All come with rice, cooked and served bubbling in a clay pot. Choose your spice level (none by default)."),
  d=[d("1-1","黄焖土豆鸡","Estofado de pollo con patata","Chicken & potato pot",9,"El clásico: pollo con patata que se deshace en la salsa.","The classic. Chicken and soft potato soaking up the sauce.","G S M",["sabroso","soja"],img="1-1"),
     d("1-2","黄焖蘑菇鸡","Estofado de pollo con champiñones","Chicken & mushroom pot",9.5,"Pollo con champiñones, más jugoso y con más sabor a seta.","Chicken with button mushrooms, juicier and earthier.","G S M",["sabroso","soja"],img="hmj"),
     d("1-3","黄焖肉","Estofado de panceta de cerdo","Pork belly pot",10,"Panceta que se deshace en la boca, con patata y setas enoki. Nada grasienta.","Melt-in-the-mouth pork belly with potato and enoki. Not greasy.","G S M",["sabroso","soja"],"p",img="1-3"),
     d("1-4","黄焖排骨","Estofado de costilla","Pork rib pot",10,"Costillas de cerdo guisadas, con patata y enoki. Lleva hueso.","Braised pork ribs with potato and enoki. Contains bones.","G S M",["sabroso","intenso"],"p",img="1-4"),
     d("1-5","黄焖牛肉","Estofado de ternera","Beef pot",11,"Ternera guisada a fuego lento: la olla más contundente.","Slow-braised beef: the heartiest pot.","G S M",["sabroso","intenso"],img="1-5"),
     d("1-6","黄焖蔬菜锅（肉汤底）","Estofado de verduras (caldo de carne)","Vegetable pot (meat broth)",9,"Patata, champiñón, enoki y pak choi, sin trozos de carne. El caldo es de carne.","Potato, mushrooms, enoki and pak choi, no pieces of meat. Meat-based broth.","G S M",["sabroso","suave"],"p",img="1-6")]),
 dict(id="sopa", zh="汤面", es="Ramen chino con caldo", en="Noodle soups",
  note=dict(zh="每一根面条都用小麦粉在店里手工制作（不是米粉）。部分汤面带香菜，不要香菜请提前跟店员说。", es="Ramen chino: fideos de harina de trigo hechos a mano en el local (no son de arroz), distintos del ramen japonés. Algunos llevan cilantro: avísanos si no lo quieres.", en="Chinese-style ramen: wheat-flour noodles handmade in-house (not rice noodles), different from Japanese ramen. Some bowls come with coriander; let us know if you'd rather skip it."),
  d=[d("2-1","清汤牛肉面","Ramen con caldo de ternera","Clear beef broth noodle soup",8.7,"Caldo claro y ligero de ternera con lonchas de carne y verdura.","Light, clear beef broth with sliced beef and greens.","G S",["suave"],img="2-1"),
     d("2-2","香菇鸡丝面","Ramen con pollo y setas shiitake","Chicken & shiitake noodle soup",9,"Pollo desmenuzado y shiitake en caldo, con huevo cocido.","Shredded chicken and shiitake in broth, with a boiled egg.","G H S M",["sabroso","suave"],img="2-2"),
     d("2-3","红烧牛肉面","Ramen con ternera estofada","Red-braised beef noodle soup",9.5,"Ternera guisada en salsa oscura de soja. Caldo intenso.","Beef braised in dark soy sauce. Full-bodied broth.","G S",["intenso","soja"],img="2-3"),
     d("2-4","麻辣肉丝面","Ramen con cerdo picante (mala)","Spicy mala pork noodle soup",9,"Tiras de cerdo en caldo rojo de chile y pimienta de Sichuan.","Pork strips in a red chilli and Sichuan pepper broth.","G S Sé",["mala"],"h p",img="2-4"),
     d("2-5","老坛酸菜牛肉面","Ramen de ternera con mostaza china encurtida","Beef & pickled greens noodle soup",9,"Ternera con mostaza china encurtida, que da un toque ácido al caldo.","Beef with Chinese pickled greens that give the broth a sour kick.","G S",["acido","sabroso"],img="2-5"),
     d("2-6","排骨汤面","Ramen con costilla","Pork rib noodle soup",9,"Costillas de cerdo guisadas, en caldo. Lleva hueso.","Braised pork ribs in broth. Contains bones.","G S",["sabroso"],"p",img="2-6"),
     d("2-7","麻辣面","Ramen picante (mala)","Spicy mala noodle soup",7.5,"Caldo de chile y pimienta de Sichuan, con huevo. Sin carne.","Chilli and Sichuan pepper broth, with egg. No meat.","G H S Sé",["mala"],"v h",img="2-7"),
     d("2-8","西红柿鸡蛋汤面","Ramen de tomate y huevo","Tomato & egg noodle soup",8.5,"Tomate y huevo revuelto en caldo: un plato casero muy querido en China.","Tomato and scrambled egg in broth: a much-loved Chinese home dish.","G H S",["agridulce","suave"],"v",img="2-8"),
     d("2-9","蔬菜汤面（肉汤底）","Ramen con verduras (caldo de carne)","Vegetable noodle soup (meat broth)",7.5,"Caldo ligero con verdura y huevo. El caldo es de carne.","Light broth with greens and egg. Meat-based broth.","G H S",["suave"],"p",img="2-9"),
     d("2-11","水煮蛋","Huevo cocido","Boiled egg",1,"Para añadir a tu cuenco.","Add to any bowl.","H",[],"v",img="2-11")]),
 dict(id="frito", zh="炒面", es="Tallarines de trigo fritos", en="Stir-fried noodles",
  note=dict(zh="店里手工做的小麦面，大火现炒，没有汤。", es="Fideos de trigo hechos a mano en el local, salteados al wok, sin caldo.", en="Handmade wheat noodles tossed in the wok, no broth."),
  d=[d("3-1","鸡蛋炒面","Tallarines de trigo fritos con huevo","Egg fried noodles",9,"Huevo, cebolla, zanahoria y repollo.","Egg, onion, carrot and cabbage.","G H S",["soja","suave"],"v",img="3-1"),
     d("3-2","肉丝炒面","Tallarines de trigo fritos con cerdo","Pork fried noodles",9.5,"Cerdo, cebolla, zanahoria y repollo.","Pork, onion, carrot and cabbage.","G S",["soja","sabroso"],"p",img="3-2"),
     d("3-3","鸡丝炒面","Tallarines de trigo fritos con pollo y shiitake","Chicken & shiitake fried noodles",9.5,"Pollo, shiitake, cebolla, zanahoria y repollo.","Chicken, shiitake, onion, carrot and cabbage.","G S M",["soja","sabroso"],img="3-3"),
     d("3-4","香辣肉丝炒面","Tallarines de trigo fritos con cerdo picante","Spicy pork fried noodles",10,"Cerdo con pimiento rojo y cilantro.","Pork with red pepper and coriander.","G S Sé",["picante"],"h p",img="3-4"),
     d("3-5","麻辣牛肉炒面","Tallarines de trigo fritos con ternera picante (mala)","Spicy mala beef fried noodles",10,"Ternera con chile y pimienta de Sichuan.","Beef with chilli and Sichuan pepper.","G S Sé",["mala"],"h",img="3-5")]),
 dict(id="insta", zh="炒方便面", es="Fideos instantáneos salteados", en="Stir-fried instant noodles",
  note=dict(zh="特色炒方便面，中国街头经典。", es="Fideos instantáneos (finos y ondulados) salteados al wok. Un clásico callejero chino.", en="Instant noodles (thin and curly) tossed in the wok. A Chinese street-food classic."),
  d=[d("4-1","西红柿鸡蛋炒方便面","Fideos instantáneos con tomate y huevo","Tomato & egg instant noodles",9,"Salteados con tomate y huevo, ligeramente dulces.","Fried with tomato and egg, slightly sweet.","G H S",["agridulce"],"v"),
     d("4-2","香辣肉丝炒方便面","Fideos instantáneos con cerdo picante","Spicy pork instant noodles",10,"Cerdo con pimiento rojo y cilantro.","Pork with red pepper and coriander.","G H S Sé",["picante"],"h p",img="4-2"),
     d("4-3","孜然肉片炒方便面","Fideos instantáneos con cerdo al comino","Cumin pork instant noodles",9.5,"Cerdo al comino, aromático y tostado.","Cumin pork, toasty and aromatic.","G H S",["comino","especias"],"p",img="4-3"),
     d("4-4","麻辣牛肉炒方便面","Fideos instantáneos con ternera picante (mala)","Spicy mala beef instant noodles",10,"Ternera con chile y pimienta de Sichuan.","Beef with chilli and Sichuan pepper.","G H S Sé",["mala"],"h",img="4-4")]),
 dict(id="mix", zh="拌面", es="Tallarines de trigo con salsa (sin caldo)", en="Dry mixed noodles",
  note=dict(zh="拌面没有汤，上桌后拌匀再吃。", es="No es una ensalada: son fideos de trigo hechos a mano en el local, sin caldo, con salsa y toppings. Mézclalos bien en el cuenco antes de comer.", en="Wheat noodles handmade in-house, with no broth, served with sauce and toppings. Mix well in the bowl before eating."),
  d=[d("5-1","鸡丝香菇拌面","Tallarines sin caldo con pollo y setas shiitake","Chicken & shiitake dry noodles",9,"Pollo, shiitake, huevo y ajo.","Chicken, shiitake, egg and garlic.","G H S M",["soja","ajo"],img="5-1"),
     d("5-2","香辣肉丝拌面","Tallarines sin caldo con cerdo picante","Spicy pork dry noodles",10,"Cerdo picante con pimiento rojo y ajo.","Spicy pork with red pepper and garlic.","G S Sé",["picante","ajo"],"h p",img="5-2"),
     d("5-3","老坛酸菜牛肉拌面","Tallarines sin caldo con ternera y mostaza china encurtida","Beef & pickled greens dry noodles",9,"Ternera y mostaza china encurtida, con un punto ácido.","Beef and pickled greens, with a sour edge.","G S",["acido","sabroso"],img="5-3"),
     d("5-4","炸酱面","Zhajiang: tallarines con pasta de soja fermentada y huevo (sin carne)","Zhajiang noodles (egg, no meat)",7.5,"Pasta de soja fermentada salteada con huevo, y pepino fresco.","Fermented bean sauce with egg and fresh cucumber.","G H S",["soja","fresco"],"v",img="5-4"),
     d("5-5","油泼面","Youpo: tallarines con aceite de chile caliente","Youpo hot chilli-oil noodles",7.5,"Aceite hirviendo sobre chile y ajo. Más aromático que picante.","Sizzling oil over chilli and garlic. More fragrant than fiery.","G S Sé",["picante","ajo"],"vg h",img="5-5")]),
 dict(id="frios", zh="凉菜 · 炒饭", es="Entrantes fríos y arroz", en="Cold starters & rice",
  note=dict(zh="可分享，也可加配。", es="Para compartir o completar tu comida.", en="To share or round off your meal."),
  d=[d("6-1","五香牛肉","Ternera a las cinco especias","Five-spice beef",6,"Fría, en lonchas. Hecha en el local.","Cold and sliced. Made in-house.","G S",["especias","fresco"],img="6-1"),
     d("6-2","凉拌黄瓜","Pepino aliñado","Cucumber salad",5,"Preparada al momento.","Made to order.","G S Sé",["fresco","ajo"],"vg",img="6-2"),
     d("6-4","凉拌海藻","Ensalada de alga wakame","Wakame salad",5,"Fresca y crujiente.","Fresh and crunchy.","G S Sé",["fresco"],"vg",img="6-4"),
     d("6-5","辣白菜","Kimchi","Kimchi",2.5,"Col fermentada picante con salsa de pescado, hecha en el local.","Spicy fermented cabbage with fish sauce, made in-house.","G S Sé P",["acido","picante"],"",img="6-5",p2=5),
     d("7-1","酱油炒饭","Arroz frito con salsa de soja","Soy sauce fried rice",7,"Arroz salteado con huevo y cebolla.","Rice wok-fried with egg and onion.","G H S",["soja"],"v",img="7-1")]),
]

CORI = [x["c"] for sec in S if sec["id"] in ("sopa", "frito", "insta", "mix")
                 for x in sec["d"] if x["c"] != "2-11"]

FIRST = [dict(c="1-1", zh="招牌黄焖鸡，不辣", es="Nuestro plato estrella, sin picante", en="Our signature, not spicy"),
         dict(c="1-6", zh="想多吃蔬菜（肉汤底）", es="Si te apetece verdura (caldo de carne)", en="If you fancy vegetables (meat broth)"),
         dict(c="5-5", zh="喜欢辣", es="Si te gusta el picante", en="If you like heat")]

EXTRAS = [[["土豆", "Patata", "Potato"], 1], [["油菜", "Pak choi", "Pak choi"], 1.2], [["白蘑菇", "Champiñón", "Button mushrooms"], 1.6], [["金针菇", "Setas enoki", "Enoki mushrooms"], 1.6], [["米饭", "Arroz", "Rice"], 1.7]]

DR = dict(beers=[["Amstel 1/3", 2.5], ["Amstel Radler 1/3", 2.5], ["Heineken", 2.5], [["青岛 Tsingtao", "Tsingtao", "Tsingtao"], 2.5], ["Águila", 2.5]],
  wine=[[["白葡萄酒（杯）", "Vino blanco de la casa (copa)", "House white wine (glass)"], 2.5], [["红葡萄酒（杯）", "Vino tinto de la casa (copa)", "House red wine (glass)"], 2.5], [["葡萄酒（整瓶）", "Botella de vino", "Bottle of wine"], 7.5]],
  soft=[[["可口可乐 / 零度", "Coca-Cola / Zero", "Coca-Cola / Zero"], 2], [["芬达 橙味 / 柠檬味", "Fanta naranja / limón", "Fanta orange / lemon"], 2], ["Nestea", 2.2], [["Aquarius 橙味 / 柠檬味", "Aquarius naranja / limón", "Aquarius orange / lemon"], 2.2], [["绿茶", "Té verde", "Green tea"], 2.5], [["红茶", "Té negro", "Black tea"], 2.5], [["王老吉凉茶", "Wanglaoji (té de hierbas)", "Wanglaoji herbal tea"], 2.5]],
  water=[[["Lanjarón 矿泉水", "Agua Lanjarón", "Lanjarón water"], 1.5]])

# 酒水示意图：[容器, 瓶身/罐身色, 标签色]
# bot 玻璃瓶（1/3，啤酒）· can 铁听 · pet 塑料瓶 · glass 高脚杯 · wbot 整瓶葡萄酒
DRILL = {
 "dr-beers-0": ["bot", "#2f6b35", "#c8352b"],   # Amstel
 "dr-beers-1": ["bot", "#2f6b35", "#e8b62c"],   # Amstel Radler 柠檬
 "dr-beers-2": ["bot", "#17683c", "#f1ece0"],   # Heineken
 "dr-beers-3": ["bot", "#2f6b35", "#1d4f8f"],   # 青岛
 "dr-beers-4": ["bot", "#8a4a1c", "#c8352b"],   # Águila（棕瓶）
 "dr-wine-0":  ["glass", "#e4ce63", ""],        # 白葡萄酒（杯）
 "dr-wine-1":  ["glass", "#8e2340", ""],        # 红葡萄酒（杯）
 "dr-wine-2":  ["wbot", "#23402a", "#e8ded0"],  # 整瓶
 "dr-soft-0":  ["can", "#c8352b", "#f1ece0"],   # 可乐
 "dr-soft-1":  ["can", "#e8742a", "#f1ece0"],   # 芬达
 "dr-soft-2":  ["can", "#d9a441", "#8a4a1c"],   # Nestea
 "dr-soft-3":  ["can", "#3f86c4", "#f1ece0"],   # Aquarius
 "dr-soft-4":  ["pet", "#4f9a4a", "#f1ece0"],   # 绿茶
 "dr-soft-5":  ["pet", "#7a4a24", "#f1ece0"],   # 红茶
 "dr-soft-6":  ["can", "#cf2a22", "#e8b62c"],   # 王老吉
 "dr-water-0": ["pet", "#9fc9e0", "#2f6b9a"]}
# 同一行里长得不一样的那几款
DRILLV = {"ccz": ["can", "#1d1d1d", "#c8352b"]}

SIDE = {"6-1": [["五香牛肉", "Ternera a las cinco especias", "Five-spice beef"], 6],
        "6-2": [["凉拌黄瓜", "Pepino aliñado", "Cucumber salad"], 5],
        "6-4": [["凉拌海藻", "Ensalada de alga wakame", "Wakame salad"], 5],
        "6-5s": [["辣白菜（小份）", "Kimchi (ración pequeña)", "Kimchi (small)"], 2.5]}
DRK = {"ts": [["青岛啤酒", "Tsingtao", "Tsingtao"], 2.5], "am": [["Amstel", "Amstel", "Amstel"], 2.5],
       "hk": [["喜力 Heineken", "Heineken", "Heineken"], 2.5], "ag": [["Águila", "Águila", "Águila"], 2.5],
       "rd": [["Amstel Radler 柠檬啤酒", "Amstel Radler (limón)", "Amstel Radler (lemon)"], 2.5],
       "cc": [["可口可乐", "Coca-Cola", "Coca-Cola"], 2], "ccz": [["Coca-Cola Zero", "Coca-Cola Zero", "Coke Zero"], 2],
       "fa": [["芬达橙味", "Fanta naranja", "Fanta Orange"], 2], "wl": [["王老吉凉茶", "Wanglaoji (té de hierbas)", "Wanglaoji herbal tea"], 2.5],
       "gt": [["绿茶", "Té verde", "Green tea"], 2.5], "ne": [["Nestea 冰红茶", "Nestea", "Nestea"], 2.2],
       "aq": [["Aquarius 柠檬味", "Aquarius limón", "Aquarius lemon"], 2.2]}

# 推荐加点里的饮料 -> 酒水单上的那一行（点推荐时加进单子的就是这一行）
DRKMAP = {"ts": "dr-beers-3", "am": "dr-beers-0", "hk": "dr-beers-2", "ag": "dr-beers-4",
          "rd": "dr-beers-1", "cc": "dr-soft-0", "ccz": "dr-soft-0", "fa": "dr-soft-1",
          "wl": "dr-soft-6", "gt": "dr-soft-4", "ne": "dr-soft-2", "aq": "dr-soft-3"}

# code: side, [beer, soft], soup-mode, reasons zh/es/en
PR = {
 "1-1": ["6-5s", ["ts", "ccz"], 0, "招牌黄焖鸡，配一碟酸辣的辣白菜解腻，再来一瓶冰啤酒或一罐零度可乐。", "Nuestro plato estrella con un poco de kimchi para equilibrar, y una cerveza fría o una Coca-Cola Zero.", "Our signature pot with a little kimchi to cut the richness, plus a cold beer or a Coke Zero."],
 "1-2": ["6-5s", ["am", "ccz"], 0, "蘑菇鸡咸鲜下饭，配一碟辣白菜开胃，再来一瓶冰饮。", "El pollo con champiñones pide un poco de kimchi y algo fresquito.", "Mushroom chicken calls for a little kimchi and something cold."],
 "1-3": ["6-4", ["hk", "cc"], 0, "软嫩的五花肉配一碟清爽的凉拌海藻，一浓一清，再加一瓶冰饮。", "La panceta, con un alga fresca para equilibrar y una bebida fría.", "Pork belly with a fresh seaweed salad for balance and a cold drink."],
 "1-4": ["6-5s", ["ts", "ccz"], 0, "慢慢啃排骨，配一碟辣白菜解腻，再来一瓶冰啤酒或零度可乐。", "Costillas sin prisa, kimchi para equilibrar y una cerveza o Coca-Cola Zero.", "Ribs to take your time over, kimchi for balance, and a beer or Coke Zero."],
 "1-5": ["6-4", ["hk", "ccz"], 0, "焖牛肉味道厚，配一碟清爽的凉拌海藻，再加一瓶冰饮。", "La ternera es intensa: un alga fresca y una bebida fría la acompañan bien.", "Rich beef pairs well with fresh seaweed and a cold drink."],
 "1-6": ["6-4", ["ag", "ne"], 0, "蔬菜锅配一碟清爽的凉拌海藻，饮料来一瓶 Águila 或冰红茶。", "La olla de verduras con un alga fresca y una Águila o un Nestea.", "The vegetable pot with fresh seaweed and an Águila or a Nestea."],
 "2-1": ["6-1", ["am", "aq"], 1, "清汤面已经有汤了，不如加一份有嚼劲的五香牛肉，让这一餐更丰富。", "Ya tienes caldo: añade ternera a las cinco especias para una comida más completa.", "You've already got broth, so add five-spice beef for a fuller meal."],
 "2-2": ["6-4", ["hk", "ne"], 1, "温和的鸡丝汤面，配一碟清爽的凉拌海藻，一热一凉刚刚好。", "Un cuenco suave con un alga fresca: caliente y frío, perfecto.", "A gentle bowl with cold seaweed: hot and cold, just right."],
 "2-3": ["6-5s", ["ts", "ccz"], 1, "红烧牛肉汤浓味厚，配一小碟酸辣的辣白菜，解腻又开胃。", "Caldo intenso y un poco de kimchi para refrescar.", "A rich broth with a little kimchi to freshen things up."],
 "2-4": ["6-2", ["rd", "wl"], 0, "麻辣汤面一定要备好「灭火器」：一碟凉拌黄瓜降温，再来一瓶冰的柠檬啤酒或王老吉。", "Con el mala hay que tener extintor: pepino fresco y una Radler fría o un Wanglaoji.", "Mala needs a fire extinguisher: cool cucumber plus a cold Radler or Wanglaoji."],
 "2-5": ["6-1", ["ag", "aq"], 1, "酸菜面酸爽开胃，加一份五香牛肉，肉量直接翻倍。", "Añade ternera a las cinco especias y tendrás el doble de carne.", "Add five-spice beef and you double the meat."],
 "2-6": ["6-5s", ["am", "cc"], 1, "排骨汤面配一小碟辣白菜，酸辣开胃。", "Costillas con un poco de kimchi para abrir el apetito.", "Ribs with a little kimchi to wake up the palate."],
 "2-7": ["6-4", ["ts", "cc"], 0, "麻辣汤面吃着会越来越热，来一瓶冰啤酒或一罐冰可乐，再配一碟清爽的海藻。", "El mala calienta cada vez más: cerveza o Coca-Cola bien fría y un alga fresca.", "Mala gets hotter as you go: an ice-cold beer or Coke and fresh seaweed."],
 "2-8": ["6-4", ["hk", "fa"], 1, "酸甜的西红柿鸡蛋面，配一碟清爽的凉拌海藻，适合不吃辣的朋友。", "Tomate y huevo con un alga fresca: ideal sin picante.", "Tomato and egg with fresh seaweed: perfect without spice."],
 "2-9": ["6-5s", ["am", "gt"], 1, "清淡的蔬菜面，加一小碟辣白菜，味道一下子就丰富了。", "Un poco de kimchi y estos fideos suaves ganan mucho sabor.", "A little kimchi gives this mild bowl a lift."],
 "3-1": ["6-5s", ["ag", "fa"], 0, "带锅气的鸡蛋炒面，配一碟辣白菜，再来一瓶冰饮。", "Fideos al wok con kimchi y una bebida fría.", "Wok-fried noodles with kimchi and a cold drink."],
 "3-2": ["6-4", ["am", "ccz"], 0, "炒面配冰啤酒或可乐，是不会出错的组合，再加一碟清爽的海藻。", "Fideos salteados y cerveza o Coca-Cola: no falla. Y un alga fresca.", "Fried noodles with beer or Coke never fails. Add fresh seaweed."],
 "3-3": ["6-1", ["hk", "ne"], 0, "香菇鸡丝炒面配一份五香牛肉，一个人也能吃出小馆子的感觉。", "Con ternera a las cinco especias, comes como en un restaurante de barrio en China.", "With five-spice beef, it's a proper Chinese neighbourhood meal, even for one."],
 "3-4": ["6-2", ["ts", "ccz"], 0, "香辣炒面配一瓶冰青岛或零度可乐，再来凉拌黄瓜降降温。", "Picante: Tsingtao o Coca-Cola Zero bien fría y pepino para refrescar.", "Spicy: an ice-cold Tsingtao or Coke Zero and cucumber to cool down."],
 "3-5": ["6-4", ["rd", "wl"], 0, "麻辣牛肉炒面很够味，配清爽的海藻，饮料来一瓶柠檬啤酒或王老吉。", "Mucho sabor mala: alga fresca y una Radler o un Wanglaoji.", "Big mala flavour: fresh seaweed and a Radler or Wanglaoji."],
 "4-1": ["6-4", ["am", "cc"], 0, "番茄鸡蛋炒方便面是街头小吃的味道，配一罐冰可乐或一瓶 Amstel，再加一碟清爽的海藻。", "Sabor de puesto callejero: Coca-Cola o Amstel bien fría y un alga fresca.", "Street-food flavour: an ice-cold Coke or Amstel and fresh seaweed."],
 "4-2": ["6-5s", ["ag", "ccz"], 0, "香辣方便面配一瓶冰 Águila 或零度可乐，再加一小碟辣白菜。", "Con una Águila o Coca-Cola Zero fría y un poco de kimchi.", "With a cold Águila or Coke Zero and a little kimchi."],
 "4-3": ["6-1", ["ts", "cc"], 0, "孜然是夜市烤串的味道，夜市当然要配一瓶冰饮和一份五香牛肉。", "El comino sabe a mercado nocturno, y eso pide una bebida fría y ternera a las cinco especias.", "Cumin tastes of night markets, which call for a cold drink and five-spice beef."],
 "4-4": ["6-4", ["hk", "wl"], 0, "麻辣方便面配一瓶冰喜力或王老吉，再加清爽的海藻。", "Mala con Heineken fría o Wanglaoji y un alga fresca.", "Mala with a cold Heineken or Wanglaoji and fresh seaweed."],
 "5-1": ["6-5s", ["am", "gt"], 0, "香菇鸡丝拌面酱香浓，配一小碟辣白菜开胃。", "Fideos con salsa intensa y un poco de kimchi para abrir el apetito.", "Rich sauced noodles with a little kimchi."],
 "5-2": ["6-4", ["ag", "ccz"], 0, "香辣拌面配一瓶冰 Águila 或零度可乐，再加清爽的海藻。", "Picante con Águila o Coca-Cola Zero fría y un alga fresca.", "Spicy, with a cold Águila or Coke Zero and fresh seaweed."],
 "5-3": ["6-1", ["hk", "aq"], 0, "酸菜牛肉拌面配一份五香牛肉，酸香里再加一份肉香。", "Más carne: ternera a las cinco especias junto a lo ácido de la mostaza encurtida.", "More meat: five-spice beef alongside the tangy pickles."],
 "5-4": ["6-5s", ["ts", "gt"], 0, "炸酱面酱香浓，配一小碟辣白菜开胃。", "Salsa intensa con un poco de kimchi para abrir el apetito.", "Rich sauce with a little kimchi to wake up the palate."],
 "5-5": ["6-2", ["rd", "ne"], 0, "油泼面香辣，配凉拌黄瓜降温，饮料来一瓶柠檬啤酒或冰红茶。全素搭配。", "Aceite de chile, pepino para refrescar y una Radler o un Nestea. Combinación vegana.", "Chilli oil, cool cucumber and a Radler or Nestea. A vegan combo."],
 "7-1": ["6-1", ["am", "cc"], 0, "酱油炒饭配一份五香牛肉，再来一瓶冰 Amstel 或可乐，简单的快乐。", "Arroz frito, ternera a las cinco especias y una Amstel o Coca-Cola fría: felicidad sencilla.", "Fried rice, five-spice beef and a cold Amstel or Coke: simple happiness."],
}

# --- 点单（购物车）---------------------------------------------------------
# 辣度（只用于黄焖锅 1-x），顺序即菜单上的顺序，默认第一个
# 可以要求不放香菜的菜：所有面（汤面 / 炒面 / 炒方便面 / 拌面），2-11 水煮蛋除外。
# 放在 S 定义之后计算，加新面时自动包含。

SP = [["不辣", "Sin picante", "None"], ["微辣", "Suave", "Mild"],
      ["中辣", "Medio", "Medium"], ["特辣", "Muy picante", "Extra hot"]]

# 购物车界面文字。中文块（给店员看的那部分）不走这里，固定中文写在 app.js.tpl 里。
CT = {
 "zh": dict(optEdit="调整", canNoCo="可以不要香菜", splitOne="只调整其中 1 份", toTop="回到顶部", addT="还要加点什么吗？", addD="来杯喝的？", sideL="小菜", otherSide="＋ 加小菜", pickDone="完成", otherDrink="＋ 加饮料", pickSide="加小菜", pickDrink="加饮料", drinkPick="饮料", noDrink="不要饮料", combo="这一套都加上", extras="加配菜", noCo="不要香菜", pick="加入我的单子", view="查看我的单子", title="我的单子", items="%s 份", item1="1 份", total="合计",
   spice="辣度", staff="给店员看 ›", copy="复制", copied="已复制", clear="清空", back="继续点菜",
   empty="还没有选菜。在菜单上点 ＋ 就可以加进来。",
   notOrder="这是一份清单，还没有下单。选好后把手机给店员看就行。",
   priceNote="价格仅供参考，最终以店员确认为准。",
   staffNote="客人自己选的，还没下单"),
 "es": dict(optEdit="Personalizar", canNoCo="Puedes pedirlo sin cilantro", splitOne="Personalizar solo 1", toTop="Volver arriba", addT="¿Añades algo más?", addD="¿Algo para beber?", sideL="Entrante", otherSide="+ Entrante", pickDone="Hecho", otherDrink="+ Bebida", pickSide="Añadir entrante", pickDrink="Añadir bebida", drinkPick="Bebida", noDrink="Sin bebida", combo="Añadir el combo", extras="Extras", noCo="Sin cilantro", pick="Añadir a mi pedido", view="Ver mi pedido", title="Mi pedido", items="%s platos", item1="1 plato", total="Total",
   spice="Picante", staff="Enseñar al personal ›", copy="Copiar", copied="Copiado", clear="Vaciar", back="Seguir pidiendo",
   empty="Aún no has elegido nada. Pulsa ＋ en cualquier plato para añadirlo.",
   notOrder="Esto es solo una lista: el pedido todavía no está hecho. Cuando lo tengas, enséñaselo al personal.",
   priceNote="Precios orientativos; el personal confirma el total.",
   staffNote="Lista hecha por el cliente, aún sin pedir"),
 "en": dict(optEdit="Customise", canNoCo="Can come without coriander", splitOne="Customise just 1", toTop="Back to top", addT="Anything else?", addD="Something to drink?", sideL="Side", otherSide="+ Side", pickDone="Done", otherDrink="+ Drink", pickSide="Add a side", pickDrink="Add a drink", drinkPick="Drink", noDrink="No drink", combo="Add this combo", extras="Extras", noCo="No coriander", pick="Add to my order", view="View my order", title="My order", items="%s items", item1="1 item", total="Total",
   spice="Spice", staff="Show to staff ›", copy="Copy", copied="Copied", clear="Clear", back="Keep choosing",
   empty="Nothing chosen yet. Tap ＋ on any dish to add it.",
   notOrder="This is just a list — nothing has been ordered yet. When you're ready, show it to our staff.",
   priceNote="Prices are a guide; staff confirm the total.",
   staffNote="Lista hecha por el cliente, aún sin pedir"),
}


# --- 店铺信息 -------------------------------------------------------------
# 统计上报地址（Cloudflare Worker 的 /c）。留空就完全不上报，一行都不发
STATS = "https://sibisi-stats.cartaviva.workers.dev/c"

# 页脚署名：品牌名和作品页地址只在这里改
BRAND = "Carta Viva"
BYURL = "https://hao1992.github.io/cartaviva/"

TEL = "+34671343226"
MAP = "https://maps.app.goo.gl/jDEgD1ig8q6Gt72TA"
REV = "https://www.google.com/search?q=Sibisi+restaurant+ramen+Valencia#lrd=0xd604ff2c6100665:0x904337579649cf0,3,,,"

# 结算前的加点推荐：出餐快、毛利高。凉拌黄瓜现做费时，不放进来。
UPSELL = ["6-5|s", "2-11", "6-4", "6-1"]

# 店主说最多人点的三道（2026-11-03）
TOP = ["1-1", "2-3", "5-1"]

# 给店员的单子按出餐分组：辣白菜、海藻和酒水前台出，其余（锅、面、炒饭、
# 五香牛肉、凉拌黄瓜）厨房做
FRONT = ["6-4", "6-5"]
GRP = {"k": "厨房", "f": "前台"}

# 多人组合：固定搭配，一键加全，价格按菜单价现算，不另打折。
# items 里的 key 就是购物车的 key：饮料是 dr-<区>-<序号>|<饮料码>，菜是 <菜号> 或 <菜号>|<大小>
COMBO = [
 dict(id="p2", n=2, zh="两人 · 经典", es="Para dos · clásico", en="For two · classic",
   zh2="一个锅配一碗面：锅里含米饭，面带汤，两个人刚好。默认不辣。",
   es2="Una olla y un cuenco de fideos: la olla lleva arroz y los fideos caldo. Sin picante.",
   en2="One pot and one noodle bowl: the pot comes with rice, the noodles with broth. Not spicy.",
   items=[["1-1", 1], ["2-3", 1], ["6-5|s", 1], ["dr-beers-3|ts", 1], ["dr-soft-0|ccz", 1]]),
 dict(id="p2h", n=2, zh="两人 · 想吃辣", es="Para dos · con picante", en="For two · with heat",
   zh2="一辣一不辣，配清爽的凉拌海藻和两瓶冰的。",
   es2="Uno picante y otro sin picante, con alga fresca y dos bebidas frías.",
   en2="One spicy, one not, with fresh seaweed salad and two cold drinks.",
   items=[["1-1", 1], ["2-4", 1], ["6-4", 1], ["dr-beers-1|rd", 1], ["dr-soft-6|wl", 1]]),
 dict(id="p4", n=4, zh="一桌 · 三到四人", es="Para la mesa · 3 o 4", en="For the table · 3–4",
   zh2="两个锅两碗面分着吃，再来两份出餐快的小菜。",
   es2="Dos ollas y dos platos de fideos para compartir, con dos entrantes fríos.",
   en2="Two pots and two noodle dishes to share, with two cold starters.",
   items=[["1-1", 1], ["1-3", 1], ["2-3", 1], ["5-1", 1], ["6-1", 1], ["6-4", 1],
          ["dr-beers-0|am", 2], ["dr-soft-0|cc", 2]]),
]

HOURS = [
 dict(d=[1, 2, 3], zh="周一至周三", es="Lun–Mié", en="Mon–Wed",
   h=dict(zh="12:30–16:30", es="12:30–16:30", en="12:30–16:30")),
 dict(d=[4], zh="周四", es="Jueves", en="Thursday",
   h=dict(zh="休息", es="Cerrado", en="Closed")),
 dict(d=[5, 6, 0], zh="周五至周日", es="Vie–Dom", en="Fri–Sun",
   h=dict(zh="12:30–16:30 · 20:00–23:00", es="12:30–16:30 · 20:00–23:00", en="12:30–16:30 · 20:00–23:00")),
]

# --- 二十四节气 ---------------------------------------------------------
# [起始月, 起始日, 中文, 拼音, 西语释义, 英语释义, 口味倾向]
# 节气是按太阳位置算的，全球同一天，瓦伦西亚也适用；但"这天吃什么"说的是中国北方的习惯。
JQ = [
 [1, 6, "小寒", "Xiǎohán", "Frío menor", "Minor cold", "hot", "ice"],
 [1, 20, "大寒", "Dàhán", "Gran frío", "Major cold", "hot", "ice"],
 [2, 4, "立春", "Lìchūn", "Comienza la primavera", "Start of spring", "light", "sprout"],
 [2, 19, "雨水", "Yǔshuǐ", "Agua de lluvia", "Rain water", "light", "rain"],
 [3, 5, "惊蛰", "Jīngzhé", "Despertar de los insectos", "Insects awaken", "light", "bug"],
 [3, 20, "春分", "Chūnfēn", "Equinoccio de primavera", "Spring equinox", "light", "balance"],
 [4, 5, "清明", "Qīngmíng", "Claro y luminoso", "Clear and bright", "spicy", "leaf"],
 [4, 20, "谷雨", "Gǔyǔ", "Lluvia de grano", "Grain rain", "spicy", "rain"],
 [5, 5, "立夏", "Lìxià", "Comienza el verano", "Start of summer", "light", "leaf"],
 [5, 21, "小满", "Xiǎomǎn", "Grano casi lleno", "Grain buds", "cold", "grain"],
 [6, 6, "芒种", "Mángzhòng", "Grano en espiga", "Grain in ear", "cold", "grain"],
 [6, 21, "夏至", "Xiàzhì", "Solsticio de verano", "Summer solstice", "cold", "sun"],
 [7, 7, "小暑", "Xiǎoshǔ", "Calor menor", "Minor heat", "cold", "hotsun"],
 [7, 23, "大暑", "Dàshǔ", "Gran calor", "Major heat", "cold", "hotsun"],
 [8, 7, "立秋", "Lìqiū", "Comienza el otoño", "Start of autumn", "cold", "fall"],
 [8, 23, "处暑", "Chǔshǔ", "Fin del calor", "End of heat", "warm", "fall"],
 [9, 8, "白露", "Báilù", "Rocío blanco", "White dew", "warm", "dew"],
 [9, 23, "秋分", "Qiūfēn", "Equinoccio de otoño", "Autumn equinox", "warm", "balance"],
 [10, 8, "寒露", "Hánlù", "Rocío frío", "Cold dew", "warm", "dew"],
 [10, 23, "霜降", "Shuāngjiàng", "Cae la escarcha", "Frost descends", "warm", "frost"],
 [11, 7, "立冬", "Lìdōng", "Comienza el invierno", "Start of winter", "hot", "snow"],
 [11, 22, "小雪", "Xiǎoxuě", "Nieve menor", "Minor snow", "hot", "snow"],
 [12, 7, "大雪", "Dàxuě", "Gran nieve", "Major snow", "hot", "snow"],
 [12, 22, "冬至", "Dōngzhì", "Solsticio de invierno", "Winter solstice", "hot", "moon"],
]

# 每种倾向配一句话，和挑出来的菜一起显示
JQW = {
 "hot":   ["天冷下来了，中国北方这时候讲究吃口热的。",
           "Hace frío: en el norte de China toca algo caliente.",
           "Cold weather — in northern China this is the time for something hot."],
 "warm":  ["秋天干燥，适合炖得久一点、味道厚一点的。",
           "Otoño seco: apetece algo guisado y con más sabor.",
           "Dry autumn days call for something braised and full-flavoured."],
 "light": ["春天宜清淡，先来碗温和的。",
           "En primavera, algo suave para empezar.",
           "Spring asks for something gentle."],
 "cold":  ["天热，吃点清爽的、不带汤的。",
           "Con este calor, algo fresco y sin caldo.",
           "Hot days: something fresh, without broth."],
 "spicy": ["湿气重的时候，中国人会吃点辣，发发汗。",
           "Con la humedad, en China se come picante para sudar un poco.",
           "In damp weather, Chinese cooking turns to chilli to work up a sweat."],
}

# --- 饭后签：菜单上的一个字 ---------------------------------------------
HANZI = [
 dict(c="焖", py="mèn",
  zh="火 + 闷：盖上锅盖，小火慢慢煨。我们招牌的「黄焖鸡」，名字就是这么来的。",
  es="«Fuego» + «encerrado»: tapar la olla y cocer despacio a fuego lento. De ahí viene el nombre de nuestro plato estrella, huángmèn jī.",
  en="“Fire” + “shut in”: cover the pot and let it cook slowly. That is where the name of our signature dish, huángmèn jī, comes from."),
 dict(c="面", py="miàn",
  zh="繁体写作「麵」，左边是「麥」—— 麦子。面是麦子做的，不是米做的。我们的面在店里现做。",
  es="En su forma tradicional, 麵, lleva a la izquierda 麥: trigo. Los fideos son de trigo, no de arroz. Los nuestros se hacen aquí.",
  en="Its traditional form, 麵, has 麥 on the left: wheat. Noodles are made of wheat, not rice. Ours are made here in the shop."),
 dict(c="鲜", py="xiān",
  zh="繁体「鮮」= 魚 + 羊。鱼和羊，古人觉得这两样放一起最好吃。菜单上写的「咸鲜」，说的就是这个味道。",
  es="En su forma tradicional, 鮮 = pez + cordero: para los antiguos chinos, los dos sabores más ricos juntos. Es el sabor que en la carta llamamos «salado y sabroso».",
  en="Its traditional form, 鮮, is fish + lamb: to the ancient Chinese, the two best flavours together. It is the taste we call “savoury” on the menu."),
 dict(c="汤", py="tāng",
  zh="繁体「湯」= 氵+ 昜（太阳升起，热）。「汤」最早的意思其实是热水，后来才变成现在的汤。",
  es="En su forma tradicional, 湯 = agua + «sol naciente», es decir, calor. Al principio significaba simplemente agua caliente; lo de «sopa» vino después.",
  en="Its traditional form, 湯, is water + “rising sun”, that is, heat. At first it just meant hot water; “soup” came later."),
 dict(c="拌", py="bàn",
  zh="提手旁 + 半：用手把东西拌到一起。拌面上桌先别急着吃，拌匀了才香。",
  es="«Mano» + «mitad»: mezclar dos cosas con la mano. Cuando lleguen tus fideos bàn, no empieces aún: remuévelos bien primero.",
  en="“Hand” + “half”: to mix things together by hand. When your bàn noodles arrive, don't start yet — stir them through first."),
 dict(c="炒", py="chǎo",
  zh="火字旁，右边是「少」。油要少，火要大，手要快 —— 炒面就是这么来的。",
  es="Lleva el radical de «fuego» y a la derecha «poco». Poco aceite, mucho fuego y mano rápida: así se hacen los fideos salteados.",
  en="It carries the “fire” radical, with “few” on the right. Little oil, high heat, quick hands — that is how fried noodles are made."),
 dict(c="香", py="xiāng",
  zh="上面是「禾」—— 谷子；下面本来是「甘」—— 甜。谷物煮熟时的那股味道，古人就叫它「香」。",
  es="Arriba, 禾: el cereal. Abajo, lo que era 甘: dulce. El olor del grano recién cocido: eso es 香.",
  en="On top, 禾: grain. Below, what used to be 甘: sweet. The smell of grain as it finishes cooking — that is 香."),
 dict(c="辣", py="là",
  zh="左边是「辛」—— 辛苦、辛酸都是它。中国人讲的辣，本来就带着一点疼。",
  es="A la izquierda, 辛: lo que pica, lo que cuesta, lo amargo de la vida. Para los chinos, el picante siempre llevó algo de dolor dentro.",
  en="On the left, 辛: sharp, stinging, the bitter part of life. In Chinese, heat always carried a little pain in it."),
 dict(c="酸", py="suān",
  zh="左边的「酉」是一个酒坛子。酸味是从坛子里发酵出来的 —— 我们的老坛酸菜就是这么来的。",
  es="A la izquierda, 酉: una tinaja. Lo ácido nace de la fermentación en la tinaja, igual que nuestra mostaza china encurtida.",
  en="On the left, 酉: a fermenting jar. Sourness comes out of the jar — exactly how our pickled greens are made."),
 dict(c="烧", py="shāo",
  zh="火 + 尧（高）：火要旺。但「红烧」的红不是辣，是酱油和糖熬出来的颜色。",
  es="«Fuego» + «alto»: fuego vivo. Pero el rojo de hóngshāo no es picante: es el color de la soja y el azúcar caramelizados.",
  en="“Fire” + “tall”: a strong flame. But the red in hóngshāo is not chilli — it is soy sauce and sugar, caramelised."),
 dict(c="锅", py="guō",
  zh="金字旁，本来说的是铁锅。我们用的是砂锅 —— 陶土做的，离了火还能咕嘟很久。",
  es="Lleva el radical del metal: al principio era una olla de hierro. La nuestra es de barro, y sigue burbujeando mucho después de salir del fuego.",
  en="It carries the metal radical — originally an iron pot. Ours is clay, and it keeps bubbling long after it leaves the stove."),
 dict(c="麦", py="mài",
  zh="繁体「麥」上面是麦穗，下面是一只脚。古人觉得麦子不是本地的，是从远方走过来的。",
  es="En 麥 hay una espiga arriba y un pie abajo: los antiguos chinos creían que el trigo no era de allí, que había llegado caminando desde lejos.",
  en="In 麥 there is an ear of grain above and a foot below: the ancient Chinese thought wheat was not theirs, that it had walked in from far away."),
 dict(c="筷", py="kuài",
  zh="竹字头 —— 筷子本来都是竹子做的。船家忌讳说「住」（停住），就反过来叫它「快子」。",
  es="Lleva el radical del bambú, que es de lo que se hacían. Los barqueros evitaban la palabra «parar», así que los llamaron «los rápidos».",
  en="It carries the bamboo radical — what they were made of. Boatmen avoided the word “stop”, so they called them “the quick ones” instead."),
 dict(c="食", py="shí",
  zh="我们店名的第一个字。上面像一个盖子，下面是一碗盛好的饭 —— 盖着的一碗饭，就是「食」。",
  es="La primera sílaba del nombre de nuestra casa. Arriba, una tapa; debajo, un cuenco servido: un cuenco tapado es «comida».",
  en="The first character in our name. A lid on top, a filled bowl underneath: a covered bowl of food is 食."),
]

# --- 筷子怎么拿 ---------------------------------------------------------
CHOP = [
 ["下面这根不动：夹在虎口里，尾端搁在无名指上。",
  "El de abajo no se mueve: apóyalo en el hueco entre pulgar e índice y sobre el dedo anular.",
  "The bottom stick never moves: rest it in the web of your thumb and on your ring finger."],
 ["上面这根像拿笔：拇指、食指、中指捏住。",
  "El de arriba se coge como un lápiz: pulgar, índice y corazón.",
  "Hold the top one like a pencil: thumb, index and middle finger."],
 ["只动上面那根，下面那根一直不动，两头对齐就夹住了。",
  "Mueve solo el de arriba; el de abajo se queda quieto. Cuando las puntas se juntan, ya está.",
  "Move only the top stick; the bottom one stays still. When the tips meet, you have it."],
]

# 中文客人抽到的签：和吃有关的中国话，配一句西班牙语，方便讲给同桌的西班牙朋友听
SAYING = [
 dict(zh="民以食为天", m="吃饭这件事，比天还大。",
      es="«El pueblo tiene la comida por cielo.»"),
 dict(zh="众口难调", m="一桌子人，口味永远凑不齐。",
      es="Aquí lo dicen así: «Nunca llueve a gusto de todos.»"),
 dict(zh="冬吃萝卜夏吃姜", m="后面还有一句：不劳医生开药方。跟着节气吃，身体自己知道。",
      es="«Rábano en invierno, jengibre en verano»: comer según la estación."),
 dict(zh="原汤化原食", m="煮面的那锅汤，喝一口，帮助消化。",
      es="«El caldo en que se cuece ayuda a digerir lo cocido.»"),
 dict(zh="一方水土养一方人", m="什么地方的水土，养出什么样的人、什么样的口味。",
      es="«Cada tierra cría a su gente.»"),
 dict(zh="好吃不过饺子", m="北方人心里，饺子永远排第一。",
      es="«Nada sabe mejor que unos jiaozi.»"),
 dict(zh="心急吃不了热豆腐", m="太急了什么都办不成，等一等，凉一凉。",
      es="«Con prisa no se come el tofu caliente.» Aquí dirían: las prisas nunca fueron buenas."),
 dict(zh="食不厌精，脍不厌细", m="孔子说的。他是山东人，和这家店的菜同一个地方。",
      es="Lo dijo Confucio, nacido en Shandong, de donde viene esta cocina: el grano nunca demasiado refinado, la carne nunca demasiado fina."),
 dict(zh="不时不食", m="也是孔子。不到季节的东西不吃 —— 两千多年前就讲究应季了。",
      es="Confucio otra vez: no comer nada fuera de su temporada. Hace dos mil quinientos años ya lo tenían claro."),
 dict(zh="吃面不吃蒜，香味少一半", m="北方的老话。下次试试配一瓣生蒜，是另一个味道。",
      es="Dicho del norte de China: «fideos sin ajo saben a la mitad». Pruébalo con un diente de ajo crudo."),
 dict(zh="饭后百步走，活到九十九", m="吃完别急着坐下，出门转一圈。",
      es="«Cien pasos después de comer y llegarás a los noventa y nueve.» No te sientes enseguida: sal a dar una vuelta."),
 dict(zh="唇齿留香", m="东西吃完了，味道还留在嘴里。",
      es="«El aroma se queda entre los labios y los dientes»: cuando el plato ya no está pero el sabor sigue ahí."),
 dict(zh="巧妇难为无米之炊", m="没有米，再好的厨子也做不出饭。",
      es="«Ni la mejor cocinera hace arroz sin arroz.» Aquí lo dicen así: nadie da lo que no tiene."),
 dict(zh="入乡随俗", m="到了哪儿，就跟着哪儿的规矩吃。在瓦伦西亚，饭点要晚一点。",
      es="«Allá donde fueres, haz lo que vieres.» En Valencia eso significa comer más tarde."),
]
