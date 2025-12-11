import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import hashlib
import json

class EstadoCelular(Enum):
    """Estados do desenvolvimento celular"""
    BIOASSINATURA = "bioassinatura"
    RECONSTRUCAO_GENOMA = "genoma_reconstruido"
    GAMETA_ARTIFICIAL = "gameta_artificial"
    EMBRIAO_FORMADO = "embriao_formado"
    DESENVOLVIMENTO = "desenvolvimento_embrionario"

@dataclass
class Bioassinatura:
    """Representa uma bioassinatura extraída de resíduos ou campos magnéticos"""
    id: str
    origem: str  # "cinzas" ou "holograma_magnetico"
    qualidade_reconstrucao: float  # 0.0 a 1.0
    dados_geneticos: Dict[str, List[str]]
    timestamp_coleta: float

@dataclass
class Gene:
    """Unidade genética básica"""
    cromossomo: int
    posicao: int
    alelo: str
    expressividade: float  # 0.0 a 1.0

@dataclass  
class GenomaReconstruido:
    """Genoma reconstruído a partir de bioassinaturas"""
    id: str
    origem_humana: str  # "masculino" ou "feminino"
    completude: float  # Porcentagem de genes reconstruídos
    genes: List[Gene]
    taxa_mutacao: float
    qualidade_sequenciamento: float

@dataclass
class GametaArtificial:
    """Gameta desenvolvido artificialmente"""
    id: str
    origem_genoma: str
    ploidia: int  # Haploide = 23 cromossomos
    cromossomos: Dict[int, List[Gene]]
    viabilidade: float  # 0.0 a 1.0

@dataclass
class Embriao:
    """Embrião resultante da fertilização artificial"""
    id: str
    estadio_desenvolvimento: int  # Dias de desenvolvimento
    celulas_totais: int
    taxa_divisao: float
    viabilidade_geral: float
    anomalias_detectadas: List[str]
    genotipo: Dict[str, str]

class SistemaReproducaoAvancada:
    """Sistema principal de simulação"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.embrioes = []
        self.genomas_reconstruidos = []
        self.bioassinaturas = []
        
    def extrair_bioassinatura(self, origem: str, qualidade: float) -> Bioassinatura:
        """Extrai bioassinatura de cinzas ou holograma magnético"""
        
        # Simulação de padrões genéticos baseados na origem
        padroes_geneticos = {
            "masculino": {
                "cromossomo_sexual": ["X", "Y"],
                "marcadores_tipicos": ["SRY", "AZF"],
                "expressoes_dominantes": ["testosterona", "musculatura"]
            },
            "feminino": {
                "cromossomo_sexual": ["X", "X"],
                "marcadores_tipicos": ["WNT4", "RSPO1"],
                "expressoes_dominantes": ["estrogenio", "desenvolvimento_mamario"]
            }
        }
        
        origem_humana = random.choice(["masculino", "feminino"])
        
        bioassinatura = Bioassinatura(
            id=f"bio_{hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}",
            origem=origem,
            qualidade_reconstrucao=qualidade,
            dados_geneticos=padroes_geneticos[origem_humana],
            timestamp_coleta=np.random.uniform(0, 1)
        )
        
        self.bioassinaturas.append(bioassinatura)
        return bioassinatura
    
    def reconstruir_genoma(self, bioassinatura: Bioassinatura) -> GenomaReconstruido:
        """Reconstrói genoma completo a partir de bioassinatura"""
        
        # Simulação da reconstrução genômica
        completude = min(1.0, bioassinatura.qualidade_reconstrucao * 1.2)
        completude = max(0.3, completude)  # Mínimo de 30% de reconstrução
        
        genes = []
        num_genes = int(completude * 25000)  # Aproximadamente 25% dos genes humanos
        
        for i in range(num_genes):
            gene = Gene(
                cromossomo=random.randint(1, 23),
                posicao=random.randint(1, 1000000),
                alelo=random.choice(["A", "T", "C", "G"] * 2 + ["ins", "del"]),
                expressividade=random.random()
            )
            genes.append(gene)
        
        genoma = GenomaReconstruido(
            id=f"genoma_{bioassinatura.id}",
            origem_humana="masculino" if "SRY" in bioassinatura.dados_geneticos.get("marcadores_tipicos", []) else "feminino",
            completude=completude,
            genes=genes,
            taxa_mutacao=0.001 * (1 - bioassinatura.qualidade_reconstrucao),
            qualidade_sequenciamento=bioassinatura.qualidade_reconstrucao
        )
        
        self.genomas_reconstruidos.append(genoma)
        return genoma
    
    def desenvolver_gameta(self, genoma: GenomaReconstruido) -> GametaArtificial:
        """Desenvolve gameta artificial a partir do genoma reconstruído"""
        
        # Processo de meiose artificial
        cromossomos = {}
        ploidia = 23  # Haploide
        
        # Seleciona aleatoriamente um conjunto de cromossomos para o gameta
        for crom in range(1, ploidia + 1):
            genes_cromossomo = [g for g in genoma.genes if g.cromossomo == crom]
            
            if genes_cromossomo:
                # Recombinação genética simulada
                genes_selecionados = random.sample(
                    genes_cromossomo, 
                    min(len(genes_cromossomo), random.randint(50, 200))
                )
                cromossomos[crom] = genes_selecionados
        
        viabilidade = genoma.qualidade_sequenciamento * 0.7 + random.random() * 0.3
        
        gameta = GametaArtificial(
            id=f"gameta_{genoma.id}",
            origem_genoma=genoma.id,
            ploidia=ploidia,
            cromossomos=cromossomos,
            viabilidade=min(1.0, viabilidade)
        )
        
        return gameta
    
    def fertilizar_gametas(self, gameta_masculino: GametaArtificial, 
                          gameta_feminino: GametaArtificial) -> Optional[Embriao]:
        """Realiza fertilização artificial entre gametas"""
        
        # Verifica compatibilidade básica
        if gameta_masculino.ploidia != 23 or gameta_feminino.ploidia != 23:
            return None
        
        # Combinação de cromossomos
        genotipo = {}
        anomalias = []
        
        # Simula a combinação genética
        for crom in range(1, 24):
            pai_genes = gameta_masculino.cromossomos.get(crom, [])
            mae_genes = gameta_feminino.cromossomos.get(crom, [])
            
            if pai_genes and mae_genes:
                # Herança mendeliana simplificada
                for i in range(min(len(pai_genes), len(mae_genes))):
                    if i < len(pai_genes) and i < len(mae_genes):
                        # Dominância aleatória
                        if random.random() > 0.5:
                            genotipo[f"gene_{crom}_{i}"] = pai_genes[i].alelo
                        else:
                            genotipo[f"gene_{crom}_{i}"] = mae_genes[i].alelo
        
        # Calcula viabilidade do embrião
        viabilidade_base = (gameta_masculino.viabilidade + gameta_feminino.viabilidade) / 2
        
        # Verifica anomalias cromossômicas
        if random.random() < 0.1 * (1 - viabilidade_base):
            anomalias.append("aneuploidia_simulada")
        if random.random() < 0.05 * (1 - viabilidade_base):
            anomalias.append("mutacao_recessiva_expressa")
        
        viabilidade_final = viabilidade_base * (1 - len(anomalias) * 0.2)
        
        if viabilidade_final < 0.3:
            return None  # Embrião não viável
        
        embriao = Embriao(
            id=f"embriao_{gameta_masculino.id[:4]}_{gameta_feminino.id[:4]}",
            estadio_desenvolvimento=0,
            celulas_totais=1,
            taxa_divisao=random.uniform(1.1, 1.8),
            viabilidade_geral=viabilidade_final,
            anomalias_detectadas=anomalias,
            genotipo=genotipo
        )
        
        self.embrioes.append(embriao)
        return embriao
    
    def simular_desenvolvimento(self, embriao: Embriao, dias: int) -> Embriao:
        """Simula o desenvolvimento embrionário"""
        
        for dia in range(dias):
            # Atualiza estádio de desenvolvimento
            embriao.estadio_desenvolvimento += 1
            
            # Crescimento celular exponencial
            embriao.celulas_totais = int(
                embriao.celulas_totais * embriao.taxa_divisao
            )
            
            # Chance de anomalias durante o desenvolvimento
            if random.random() < 0.05 * (1 - embriao.viabilidade_geral):
                nova_anomalia = f"anomalia_desenvolvimento_dia_{dia}"
                if nova_anomalia not in embriao.anomalias_detectadas:
                    embriao.anomalias_detectadas.append(nova_anomalia)
                    embriao.viabilidade_geral *= 0.9
            
            # Limite máximo de células
            if embriao.celulas_totais > 1000000:  # Aproximadamente estádio de blastocisto
                embriao.celulas_totais = 1000000
                embriao.taxa_divisao = 1.0  # Para de crescer
                
        return embriao

def simular_cruzamento_completo():
    """Executa simulação completa do processo"""
    
    print("=" * 80)
    print("SIMULAÇÃO DE CRUZAMENTO ARTIFICIAL AVANÇADO")
    print("Baseado em reconstrução de bioassinaturas genéticas")
    print("=" * 80)
    
    # Configuração do sistema
    config = {
        "qualidade_coleta_cinzas": 0.7,
        "qualidade_holograma_magnetico": 0.6,
        "taxa_mutacao_base": 0.001,
        "viabilidade_minima": 0.3
    }
    
    sistema = SistemaReproducaoAvancada(config)
    
    # Fase 1: Coleta de bioassinaturas
    print("\n[FASE 1] Extração de bioassinaturas")
    print("-" * 40)
    
    bio_masculina = sistema.extrair_bioassinatura(
        origem="cinzas", 
        qualidade=config["qualidade_coleta_cinzas"]
    )
    
    bio_feminina = sistema.extrair_bioassinatura(
        origem="holograma_magnetico", 
        qualidade=config["qualidade_holograma_magnetico"]
    )
    
    print(f"Bioassinatura masculina extraída: {bio_masculina.id}")
    print(f"  Origem: {bio_masculina.origem}")
    print(f"  Qualidade: {bio_masculina.qualidade_reconstrucao:.2%}")
    print(f"  Marcadores: {bio_masculina.dados_geneticos['marcadores_tipicos']}")
    
    print(f"\nBioassinatura feminina extraída: {bio_feminina.id}")
    print(f"  Origem: {bio_feminina.origem}")
    print(f"  Qualidade: {bio_feminina.qualidade_reconstrucao:.2%}")
    print(f"  Marcadores: {bio_feminina.dados_geneticos['marcadores_tipicos']}")
    
    # Fase 2: Reconstrução genômica
    print("\n[FASE 2] Reconstrução genômica")
    print("-" * 40)
    
    genoma_masculino = sistema.reconstruir_genoma(bio_masculina)
    genoma_feminino = sistema.reconstruir_genoma(bio_feminina)
    
    print(f"Genoma masculino reconstruído: {genoma_masculino.id}")
    print(f"  Completude: {genoma_masculino.completude:.2%}")
    print(f"  Genes reconstruídos: {len(genoma_masculino.genes)}")
    print(f"  Taxa de mutação: {genoma_masculino.taxa_mutacao:.4f}")
    
    print(f"\nGenoma feminino reconstruído: {genoma_feminino.id}")
    print(f"  Completude: {genoma_feminino.completude:.2%}")
    print(f"  Genes reconstruídos: {len(genoma_feminino.genes)}")
    print(f"  Taxa de mutação: {genoma_feminino.taxa_mutacao:.4f}")
    
    # Fase 3: Desenvolvimento de gametas artificiais
    print("\n[FASE 3] Desenvolvimento de gametas artificiais")
    print("-" * 40)
    
    gameta_masculino = sistema.desenvolver_gameta(genoma_masculino)
    gameta_feminino = sistema.desenvolver_gameta(genoma_feminino)
    
    print(f"Gameta masculino artificial: {gameta_masculino.id}")
    print(f"  Cromossomos ativos: {len(gameta_masculino.cromossomos)}/23")
    print(f"  Viabilidade: {gameta_masculino.viabilidade:.2%}")
    
    print(f"\nGameta feminino artificial: {gameta_feminino.id}")
    print(f"  Cromossomos ativos: {len(gameta_feminino.cromossomos)}/23")
    print(f"  Viabilidade: {gameta_feminino.viabilidade:.2%}")
    
    # Fase 4: Fertilização artificial
    print("\n[FASE 4] Fertilização artificial")
    print("-" * 40)
    
    embriao = sistema.fertilizar_gametas(gameta_masculino, gameta_feminino)
    
    if embriao:
        print(f"Embrião formado com sucesso: {embriao.id}")
        print(f"  Viabilidade inicial: {embriao.viabilidade_geral:.2%}")
        print(f"  Anomalias detectadas: {embriao.anomalias_detectadas or 'Nenhuma'}")
        print(f"  Genes combinados: {len(embriao.genotipo)}")
        
        # Fase 5: Desenvolvimento embrionário
        print("\n[FASE 5] Desenvolvimento embrionário (14 dias)")
        print("-" * 40)
        
        embriao_desenvolvido = sistema.simular_desenvolvimento(embriao, dias=14)
        
        print(f"Embrião após desenvolvimento:")
        print(f"  Estádio: {embriao_desenvolvido.estadio_desenvolvimento} dias")
        print(f"  Células totais: {embriao_desenvolvido.celulas_totais:,}")
        print(f"  Viabilidade atual: {embriao_desenvolvido.viabilidade_geral:.2%}")
        print(f"  Anomalias totais: {len(embriao_desenvolvido.anomalias_detectadas)}")
        
        if embriao_desenvolvido.viabilidade_geral >= 0.5:
            print("\n✅ RESULTADO: Embrião viável para implantação")
        else:
            print("\n⚠️  RESULTADO: Embrião com viabilidade reduzida")
            
    else:
        print("❌ Fertilização não resultou em embrião viável")
    
    # Relatório final
    print("\n" + "=" * 80)
    print("RELATÓRIO FINAL DA SIMULAÇÃO")
    print("=" * 80)
    
    estatisticas = {
        "bioassinaturas_coletadas": len(sistema.bioassinaturas),
        "genomas_reconstruidos": len(sistema.genomas_reconstruidos),
        "gametas_desenvolvidos": 2,
        "embrioes_formados": 1 if embriao else 0,
        "viabilidade_media": embriao.viabilidade_geral if embriao else 0.0
    }
    
    print(f"\nEstatísticas do processo:")
    for key, value in estatisticas.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    return sistema, embriao if embriao else None

# Executar a simulação
if __name__ == "__main__":
    sistema, embriao_resultante = simular_cruzamento_completo()
