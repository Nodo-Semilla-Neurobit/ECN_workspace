/* DELTA · ampliar la autodetección de m11 para reconocer el runbook.
   Reemplazar el auto: de m11 por este (una sola línea cambia): */
{id:"m11",nivel:4,t:"Salón plegado (e2e)",
 auto:[{cmd:/test_salon_e2e|salon_pliegue|runbook_salon/,
        out:[/E2E OK|PLEGUE MATERIALIZADO|RUNBOOK SALÓN COMPLETO|RUNBOOK SALON COMPLETO/]}],
 ev:{i:"Pegá la salida del runbook o del test e2e",rx:[/E2E OK|SALON_RUTEADO|PLEGUE_OK/]},
 s:"El salón ya no es órgano paralelo: es un radio del ecosistema."}
