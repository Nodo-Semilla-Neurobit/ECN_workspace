/* DELTA · MISIÓN m11 "SALÓN PLEGADO" para el instalador lúdico
   Pegar en el array de misiones del frontend del instalador
   (junto a m6..m10) y en MISIONES_GUIA + calcRango(nivel 4). */

/* 1) En el array de misiones (el que tiene auto:/ev:): */
{id:"m11",nivel:4,t:"Salón plegado (e2e)",
 auto:[{cmd:/test_salon_e2e|salon_pliegue/,out:[/E2E OK|PLEGUE MATERIALIZADO/]}],
 ev:{i:"Pegá la salida del test e2e del salón",rx:[/E2E OK|SALON_RUTEADO/]},
 s:"El salón ya no es órgano paralelo: es un radio del ecosistema."},

/* 2) En MISIONES_GUIA (guía flotante ◈): */
{id:"m11",t:"Salón plegado (e2e)",p:"bash test_salon_e2e.sh"},

/* 3) En calcRango: el nivel 4 pasa de [m9,m10] a: */
/*    ["m9","m10","m11"]  
