# -*- coding: utf-8 -*-
import time
from datetime import datetime, date
import dataset
from sqlalchemy.pool import NullPool
db = dataset.connect('sqlite:///banco.sqlite', engine_kwargs={'poolclass':NullPool} )
medicos = db['medicos']
pacientes = db['pacientes']
agendamentos = db['agendamentos']


if __name__ == '__main__':
    medico_values = {
        'nome':u'Médico de Teste',
        'crm':u'1666/2003',
        'status':True,
        'especialidade':u'Cardiologia',
        'area':u'Ecocardiografia',
        'numero':u'10-5',
        'rua':u'Rua de Teste',
        'bairro':u'Centro',
        'cidade':u'Bauru',
        'estado':u'SP',
        'telefone':u'+55 14 9 1234-5678',
        'cpf':u'111.222.444.777-35'
    }

    paciente_values = {
        'nome':u'Paciente de Teste',
        'numero':u'10-5',
        'rua':u'Rua de Teste',
        'bairro':u'Centro',
        'cidade':u'Bauru',
        'estado':u'SP',
        'telefone':u'+55 14 9 1234-5678',
        'cpf':u'111.222.444.777-35',
        'plano':u'SEM PLANO'
    }

    agendamento_values = {
        'id_medico':1,
        'id_paciente':1,
        'data':date.today(),
        'hora':datetime.strftime(datetime.now(), '%H:%M:%S'),
    }

    medicos.insert(medico_values)
    pacientes.insert(paciente_values)
    agendamentos.insert(agendamento_values)