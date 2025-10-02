import { Component, signal } from '@angular/core';
import { ApiService } from './api';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  standalone: false,
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('datacheck');

  constructor(private apiService: ApiService) { }

  // projudi: any[] = [
  //   {
  //     "STATUS": "ARQUIVADO",
  //     "CLASSE_PROCESSUAL": "EXECUÇÃO FISCAL",
  //     "ASSUNTO_PRINCIPAL": "DÍVIDA ATIVA (EXECUÇÃO FISCAL)",
  //     "NIVEL_SIGILO": "PÚBLICO",
  //     "COMARCA": "CURITIBA",
  //     "COMPETENCIA": "VARA DA FAZENDA PÚBLICA",
  //     "AUTUACAO": "29/05/2013 ÀS 12:15:59",
  //     "JUIZO": "SECRETARIA ESPECIALIZADA EM MOVIMENTAÇÕES PROCESSUAIS DAS VARAS DE EXECUÇÕES FISCAIS MUNICIPAIS DE CURITIBA - 3ª VARA",
  //     "DISTRIBUICAO": "03/06/2013 ÀS 18:44:28",
  //     "JUIZ": "ROSSELINI CARNEIRO",
  //     "DATA DE ARQUIVAMENTO": "27/05/2014 ÀS 17:29:21",
  //     "DATA DO TRANSITO EM JULGADO": "28/03/2014",
  //     "PARTES": [
  //       {
  //         "TIPO": "EXEQUENTE",
  //         "NAME": "MUNICÍPIO DE CURITIBA/PR",
  //         "OBSERVACAO": "CITAÇÃO E INTIMAÇÃO ONLINE",
  //         "ADVOGADOS": [
  //           "(PROCURADOR) OAB 31401N-PR - ANA BEATRIZ BALAN VILLELA"
  //         ]
  //       },
  //       {
  //         "TIPO": "EXECUTADO",
  //         "NAME": "LEANDRO BATISTA DE ALMEIDA",
  //         "OBSERVACAO": null,
  //         "ADVOGADOS": []
  //       }
  //     ],
  //     "MOVIMENTACOES": [
  //       {
  //         'SEQUENCIA': '32',
  //         'DATA': '24/11/2020 18:34:19',
  //         'TP_EVENTO': 'REDISTRIBUÍDO PARA COMPETÊNCIA EXCLUSIVA',
  //         'DS_EVENTO': 'ORIGEM: SECRETARIA UNIFICADA DAS VARAS DE EXECUÇÕES FISCAIS MUNICIPAIS DE CURITIBA - 2ª VARA. DESTINO: SECRETARIA UNIFICADA DAS VARAS DE EXECUÇÕES FISCAIS MUNICIPAIS DE CURITIBA - 3ª VARA. SEI - 0068461-84.2019.8.16.6000',
  //         'MOVIMENTADO': 'CLEVERLY JULIANE JUSTUS ZIELINSKI - ANALISTA JUDICIÁRIO'
  //       },
  //       {
  //         'SEQUENCIA': '31',
  //         'DATA': '19/07/2014 00:03:02',
  //         'TP_EVENTO': 'DECORRIDO PRAZO DE LEANDRO BATISTA DE ALMEIDA',
  //         'DS_EVENTO': 'REFERENTE AO PRAZO PARA CUMPRIMENTO DA CITAÇÃO',
  //         'MOVIMENTADO': 'SISTEMA PROJUDI'
  //       },
  //       {
  //         'SEQUENCIA': '30',
  //         'DATA': '18/07/2014 17:58:44',
  //         'TP_EVENTO': 'ATO CUMPRIDO PELA PARTE OU INTERESSADO',
  //         'DS_EVENTO': 'LEITURA DE CITAÇÃO REALIZADA - POR LEANDRO BATISTA DE ALMEIDA EM 24/01/2014',
  //         'MOVIMENTADO': 'RICARDO BONATO BERTO - TÉCNICO JUDICIÁRIO'
  //       },
  //       {
  //         'SEQUENCIA': '29',
  //         'DATA': '27/05/2014 17:29:21',
  //         'TP_EVENTO': 'ARQUIVADO DEFINITIVAMENTE',
  //         'DS_EVENTO': null,
  //         'MOVIMENTADO': 'HELENA IVANFY - ANALISTA JUDICIÁRIO'
  //       },
  //       {
  //         'SEQUENCIA': '28',
  //         'DATA': '15/05/2014 14:30:04',
  //         'TP_EVENTO': 'RECEBIDOS OS AUTOS',
  //         'DS_EVENTO': 'RECEBIDO DO(A) DISTRIBUIDOR',
  //         'MOVIMENTADO': 'SISTEMA PROJUDI'
  //       },
  //       {
  //         'SEQUENCIA': '27',
  //         'DATA': '15/05/2014 14:30:04',
  //         'TP_EVENTO': 'JUNTADA DE ANOTAÇÃO DE BAIXA DEFINITIVA',
  //         'DS_EVENTO': null,
  //         'MOVIMENTADO': 'THIAGO VIRISSIMO - DISTRIBUIDOR'
  //       },
  //       {
  //         'SEQUENCIA': '26',
  //         'DATA': '14/05/2014 18:31:56',
  //         'TP_EVENTO': 'REMETIDOS OS AUTOS PARA DISTRIBUIDOR',
  //         'DS_EVENTO': 'BAIXA',
  //         'MOVIMENTADO': 'GABRIELLE RAUCHBACH MARIOTTI - TÉCNICO JUDICIÁRIO'
  //       },
  //       {
  //         'SEQUENCIA': '25',
  //         'DATA': '14/05/2014 18:31:50',
  //         'TP_EVENTO': 'TRANSITADO EM JULGADO EM 28/03/2014',
  //         'DS_EVENTO': 'PARA O PROCESSO.',
  //         'MOVIMENTADO': 'GABRIELLE RAUCHBACH MARIOTTI - TÉCNICO JUDICIÁRIO'
  //       },
  //       {
  //         'SEQUENCIA': '24',
  //         'DATA': '14/05/2014 18:31:50',
  //         'TP_EVENTO': 'TRANSITADO EM JULGADO EM 28/03/2014',
  //         'DS_EVENTO': 'EM 28/03/2014 PARA MUNICÍPIO DE CURITIBA/PR.',
  //         'MOVIMENTADO': 'GABRIELLE RAUCHBACH MARIOTTI - TÉCNICO JUDICIÁRIO'
  //       }
  //     ]
  //   },
  // ]

  projudi: any[] = [];

  isLoading = false;

  expandedItems: Set<string> = new Set();

  toggle(item: string) {
    if (this.expandedItems.has(item)) {
      this.expandedItems.delete(item);
    } else {
      this.expandedItems.add(item);
    }
  }

  isExpanded(item: string): boolean {
    return this.expandedItems.has(item);
  }

  consultar(cpf: any, nome: any, nascimento: any) {
    this.isLoading = true;

    this.apiService.getPessoa(cpf, nome, nascimento).subscribe({
      next: (res) => {
        console.log(res);
        this.projudi = res?.projudi?.data
        this.isLoading = false;
      },
      error: () => this.isLoading = false
    });
  }
}
