// src/swagger.js

import swaggerJsdoc from 'swagger-jsdoc';
import path from 'path';
import { fileURLToPath } from 'url';
import {EXTERNAL_URL} from './src/env.js'; 


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const options = {
    swaggerDefinition: {
        openapi: '3.0.0',
        info: {
            title: 'API do Bot Discord',
            version: '1.0.0',
            description: 'API para controlar o bot do Discord via comandos HTTP',
        },
        servers: [
            {
                url: `${EXTERNAL_URL}/api`,
                description: 'Servidor de Desenvolvimento',
            },
        ],
    },
    // O curinga '**/*.yaml' procura por todos os arquivos .yaml
    // dentro de 'src/routes' e seus subdiretórios.
    apis: [path.join(__dirname, 'src', '**', '*.yaml')],
};

const swaggerSpec = swaggerJsdoc(options);
export default swaggerSpec;