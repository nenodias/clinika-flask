# -*- coding: utf-8 -*-
import time
from datetime import datetime, date
import dataset
from sqlalchemy.pool import NullPool
db = dataset.connect('sqlite:///banco.sqlite', engine_kwargs={'poolclass':NullPool} )

especialidades = db['especialidades']
medicos = db['medicos']
pacientes = db['pacientes']
agendamentos = db['agendamentos']


if __name__ == '__main__':
    especialidade_values ={
        'descricao':u'',
        'status':True,

    }
    medico_values = {
        'nome':u'Médico de Teste',
        'cpf':u'111.222.444.777-35',
        'crm':u'1666/2003',
        'status':True,
        'id_especialidade':1,
        'area':u'Ecocardiografia',
        'numero':u'10-5',
        'rua':u'Rua de Teste',
        'bairro':u'Centro',
        'cidade':u'Bauru',
        'estado':u'SP',
        'telefone':u'+55 14 9 1234-5678',
    }

    paciente_values = {
        'nome':u'Paciente de Teste',
        'cpf':u'111.222.444.777-35',
        'telefone':u'+55 14 9 1234-5678',
        'plano':u'SEM PLANO',
        'rua':u'Rua de Teste',
        'numero':u'10-5',
        'bairro':u'Centro',
        'cidade':u'Bauru',
        'estado':u'SP',
    }

    agendamento_values = {
        'id_medico':1,
        'id_paciente':1,
        'data':date.today(),
        'hora':datetime.strftime(datetime.now(), '%H:%M:%S'),
    }

    #results = medicos.find(_limit=10,_offset=1)
    especialidades.insert(especialidade_values)
    medicos.insert(medico_values)
    pacientes.insert(paciente_values)
    agendamentos.insert(agendamento_values)