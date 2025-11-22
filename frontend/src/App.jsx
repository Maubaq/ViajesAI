import React, { useState, useEffect } from 'react';
import axios from 'axios';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './App.css';

// Función para renderizar markdown simple (negritas y bullets)
const renderMarkdown = (text) => {
  if (!text) return '';
  
  // Función auxiliar para procesar negritas en un texto
  const processBold = (text, lineIndex) => {
    const parts = [];
    let lastIndex = 0;
    const boldRegex = /\*\*(.*?)\*\*/g;
    let match;
    let boldIndex = 0;
    
    while ((match = boldRegex.exec(text)) !== null) {
      // Agregar texto antes del match
      if (match.index > lastIndex) {
        parts.push(text.substring(lastIndex, match.index));
      }
      // Agregar texto en negrita
      parts.push(<strong key={`bold-${lineIndex}-${boldIndex++}`}>{match[1]}</strong>);
      lastIndex = match.index + match[0].length;
    }
    
    // Agregar texto restante
    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }
    
    return parts.length > 0 ? parts : text;
  };
  
  // Dividir por líneas
  const lines = text.split('\n');
  const result = [];
  let currentSection = null;
  let sectionContent = [];
  
  lines.forEach((line, index) => {
    const trimmedLine = line.trim();
    
    // Detectar inicio de sección con emojis (🏨 🍽️ 📍 💡 💰)
    const sectionMatch = trimmedLine.match(/^([🏨🍽️📍💡💰])\s+\*\*(.+?):\*\*/);
    
    if (sectionMatch) {
      // Si hay una sección anterior, renderizarla
      if (currentSection) {
        result.push(
          <div key={`section-${currentSection.index}`} className="response-section">
            <div className="section-header">
              <span className="section-symbol">{currentSection.symbol}</span>
              <span className="section-title">{currentSection.title}</span>
            </div>
            <div className="section-content">
              {sectionContent.map((content, idx) => (
                <div key={idx}>{content}</div>
              ))}
            </div>
          </div>
        );
      }
      
      // Iniciar nueva sección
      const symbol = sectionMatch[1];
      const title = sectionMatch[2];
      const content = trimmedLine.replace(/^[🏨🍽️📍💡💰]\s+\*\*.+?:\*\*\s*/, '');
      
      currentSection = { symbol, title, index };
      sectionContent = [];
      
      if (content) {
        sectionContent.push(processBold(content, index));
      }
    } else if (currentSection) {
      // Línea dentro de una sección
      if (trimmedLine === '') {
        sectionContent.push(<br key={`br-${index}`} />);
      } else {
        // Detectar bullets dentro de la sección
        const bulletMatch = trimmedLine.match(/^(?:[•\-\*]|\d+\.)\s+(.+)/);
        if (bulletMatch) {
          sectionContent.push(
            <div key={`bullet-${index}`} className="response-bullet">
              • {processBold(bulletMatch[1], index)}
            </div>
          );
        } else {
          sectionContent.push(
            <div key={`line-${index}`} className="response-line">
              {processBold(trimmedLine, index)}
            </div>
          );
        }
      }
    } else {
      // Línea fuera de sección
      if (trimmedLine === '') {
        result.push(<br key={`line-${index}`} />);
      } else {
        const bulletMatch = trimmedLine.match(/^(?:[•\-\*]|\d+\.)\s+(.+)/);
        if (bulletMatch) {
          result.push(
            <div key={`line-${index}`} className="response-bullet">
              • {processBold(bulletMatch[1], index)}
            </div>
          );
        } else {
          result.push(
            <div key={`line-${index}`} className="response-line">
              {processBold(trimmedLine, index)}
            </div>
          );
        }
      }
    }
  });
  
  // Renderizar última sección si existe
  if (currentSection) {
    result.push(
      <div key={`section-${currentSection.index}`} className="response-section">
        <div className="section-header">
          <span className="section-symbol">{currentSection.symbol}</span>
          <span className="section-title">{currentSection.title}</span>
        </div>
        <div className="section-content">
          {sectionContent.map((content, idx) => (
            <div key={idx}>{content}</div>
          ))}
        </div>
      </div>
    );
  }
  
  return result;
};

function App() {
  const [showForm, setShowForm] = useState(true);
  const [formData, setFormData] = useState({
    destino: '',
    fechaInicio: '',
    fechaFin: '',
    presupuesto: '',
    preferencia: ''
  });
  const [question, setQuestion] = useState('');
  const [followUpQuestion, setFollowUpQuestion] = useState('');
  const [responses, setResponses] = useState([]); // Array de respuestas para el chat continuo
  const [clima, setClima] = useState(null);
  const [fotos, setFotos] = useState([]);
  const [destino, setDestino] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [infoAdicional, setInfoAdicional] = useState(null);
  const [horaActual, setHoraActual] = useState(new Date());
  const [historial, setHistorial] = useState([]);
  const [favoritos, setFavoritos] = useState([]);
  
  // Cargar favoritos desde localStorage al iniciar
  useEffect(() => {
    const favoritosGuardados = localStorage.getItem('viajeia_favoritos');
    if (favoritosGuardados) {
      try {
        setFavoritos(JSON.parse(favoritosGuardados));
      } catch (e) {
        console.error('Error cargando favoritos:', e);
      }
    }
  }, []);
  
  // Guardar favoritos en localStorage cuando cambien
  useEffect(() => {
    if (favoritos.length > 0) {
      localStorage.setItem('viajeia_favoritos', JSON.stringify(favoritos));
    }
  }, [favoritos]);
  
  // Actualizar hora cada segundo si hay información de diferencia horaria
  useEffect(() => {
    if (infoAdicional?.diferencia_horaria) {
      const interval = setInterval(() => {
        setHoraActual(new Date());
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [infoAdicional?.diferencia_horaria]);
  
  // Función para guardar destino como favorito
  const handleGuardarFavorito = () => {
    if (!destino) return;
    
    const nuevoFavorito = {
      destino: destino,
      fechaGuardado: new Date().toISOString(),
      clima: clima,
      fotos: fotos.slice(0, 1), // Guardar solo la primera foto como preview
      infoAdicional: infoAdicional
    };
    
    // Verificar si ya existe
    const existe = favoritos.some(fav => fav.destino.toLowerCase() === destino.toLowerCase());
    
    if (!existe) {
      setFavoritos(prev => [...prev, nuevoFavorito]);
    }
  };
  
  // Función para eliminar favorito
  const handleEliminarFavorito = (destinoEliminar) => {
    setFavoritos(prev => prev.filter(fav => fav.destino !== destinoEliminar));
  };
  
  // Función para cargar un destino favorito
  const handleCargarFavorito = (favorito) => {
    setDestino(favorito.destino);
    setClima(favorito.clima);
    setFotos(favorito.fotos || []);
    setInfoAdicional(favorito.infoAdicional);
    // Limpiar respuestas y empezar de nuevo con este destino
    setResponses([]);
    setShowForm(false);
    setQuestion(`Quiero planear un viaje a ${favorito.destino}`);
  };
  
  // Función para generar PDF del itinerario usando HTML con tablas
  const generarPDF = async (conversacionEspecifica = null) => {
    try {
      // Crear elemento HTML temporal
      const pdfContainer = document.createElement('div');
      pdfContainer.style.position = 'absolute';
      pdfContainer.style.left = '-9999px';
      pdfContainer.style.width = '210mm'; // A4 width
      pdfContainer.style.padding = '20mm';
      pdfContainer.style.fontFamily = 'Arial, sans-serif';
      pdfContainer.style.backgroundColor = '#ffffff';
      pdfContainer.style.color = '#2d3748';
      document.body.appendChild(pdfContainer);
      
      const destinoTexto = destino || formData.destino || 'Destino no especificado';
      
      // Construir HTML
      let htmlContent = `
        <style>
          .pdf-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
          }
          .pdf-header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: bold;
          }
          .pdf-header p {
            margin: 5px 0 0 0;
            font-size: 12px;
          }
          .pdf-info-box {
            background: #f5f7fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
          }
          .pdf-info-box h2 {
            margin: 0 0 10px 0;
            font-size: 16px;
            color: #2d3748;
          }
          .pdf-info-box p {
            margin: 5px 0;
            font-size: 11px;
            color: #718096;
          }
          .pdf-question {
            background: #f0f2f5;
            padding: 12px;
            border-radius: 6px;
            margin: 20px 0 10px 0;
            font-weight: bold;
            color: #667eea;
          }
          .pdf-section-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            page-break-inside: avoid;
          }
          .pdf-section-header {
            background: #667eea;
            color: white;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 4px 4px 0 0;
          }
          .pdf-section-content {
            background: #ffffff;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-top: none;
            border-radius: 0 0 4px 4px;
          }
          .pdf-section-content ul {
            margin: 0;
            padding-left: 20px;
          }
          .pdf-section-content li {
            margin: 8px 0;
            line-height: 1.6;
          }
          .pdf-photos-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
          }
          .pdf-photo-item {
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            overflow: hidden;
          }
          .pdf-photo-item img {
            width: 100%;
            height: auto;
            display: block;
          }
          .pdf-photo-caption {
            padding: 8px;
            font-size: 9px;
            color: #718096;
            text-align: center;
          }
        </style>
        
        <div class="pdf-header">
          <h1>🧳 ViajeIA</h1>
          <p>Tu Asistente Personal de Viajes</p>
        </div>
        
        <div class="pdf-info-box">
          <h2>📍 Destino: ${destinoTexto}</h2>
          ${formData.fechaInicio || formData.fechaFin ? `
            <p>📅 Fechas: ${
              formData.fechaInicio 
                ? new Date(formData.fechaInicio).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' })
                : 'No especificada'
            } - ${
              formData.fechaFin
                ? new Date(formData.fechaFin).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' })
                : 'No especificada'
            }</p>
          ` : ''}
          ${clima && !conversacionEspecifica ? `
            <p>🌡️ Clima actual: ${clima.temperatura}°C - ${clima.descripcion}</p>
          ` : ''}
        </div>
      `;
      
      // Contenido de las conversaciones
      const conversaciones = conversacionEspecifica 
        ? [conversacionEspecifica]
        : responses.length > 0 
          ? responses 
          : historial.map(h => ({ pregunta: h.pregunta, respuesta: h.respuesta }));
      
      conversaciones.forEach((item, index) => {
        if (item.pregunta) {
          htmlContent += `<div class="pdf-question">❓ ${item.pregunta}</div>`;
        }
        
        if (item.respuesta) {
          let respuestaTexto = item.respuesta;
          
          // Detectar secciones estructuradas
          const secciones = [
            { nombre: 'ALOJAMIENTO:', emoji: '🏨' },
            { nombre: 'COMIDA LOCAL:', emoji: '🍽️' },
            { nombre: 'LUGARES IMPERDIBLES:', emoji: '📍' },
            { nombre: 'CONSEJOS LOCALES:', emoji: '💡' },
            { nombre: 'ESTIMACIÓN DE COSTOS:', emoji: '💰' }
          ];
          
          let tieneSecciones = false;
          for (const seccion of secciones) {
            if (respuestaTexto.includes(seccion.nombre)) {
              tieneSecciones = true;
              break;
            }
          }
          
          if (tieneSecciones) {
            // Procesar respuesta con secciones estructuradas usando tablas
            const lineas = respuestaTexto.split('\n');
            let contenidoSeccion = '';
            let seccionActual = null;
            
            for (let i = 0; i < lineas.length; i++) {
              const linea = lineas[i].trim();
              
              // Verificar si es inicio de sección
              let esInicioSeccion = false;
              for (const seccion of secciones) {
                if (linea.includes(seccion.nombre)) {
                  // Cerrar sección anterior si existe
                  if (seccionActual) {
                    htmlContent += `
                      <table class="pdf-section-table">
                        <tr>
                          <td class="pdf-section-header">${seccionActual.emoji} ${seccionActual.nombre}</td>
                        </tr>
                        <tr>
                          <td class="pdf-section-content">
                            <ul>${contenidoSeccion}</ul>
                          </td>
                        </tr>
                      </table>
                    `;
                    contenidoSeccion = '';
                  }
                  
                  esInicioSeccion = true;
                  seccionActual = seccion;
                  break;
                }
              }
              
              if (!esInicioSeccion && seccionActual && linea) {
                // Procesar contenido de la sección
                let textoProcesado = linea.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                
                // Detectar bullets
                if (linea.match(/^[•\-\*]\s+(.+)/)) {
                  const contenido = linea.replace(/^[•\-\*]\s+/, '');
                  contenidoSeccion += `<li>${textoProcesado.replace(/^[•\-\*]\s+/, '')}</li>`;
                } else if (linea.trim() && !linea.match(/^ALOJAMIENTO:|^COMIDA LOCAL:|^LUGARES IMPERDIBLES:|^CONSEJOS LOCALES:|^ESTIMACIÓN DE COSTOS:/)) {
                  contenidoSeccion += `<li>${textoProcesado}</li>`;
                }
              } else if (!esInicioSeccion && !seccionActual && linea) {
                // Texto fuera de secciones
                let textoProcesado = linea.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                htmlContent += `<p style="line-height: 1.6; margin: 10px 0;">${textoProcesado}</p>`;
              }
            }
            
            // Cerrar última sección
            if (seccionActual && contenidoSeccion) {
              htmlContent += `
                <table class="pdf-section-table">
                  <tr>
                    <td class="pdf-section-header">${seccionActual.emoji} ${seccionActual.nombre}</td>
                  </tr>
                  <tr>
                    <td class="pdf-section-content">
                      <ul>${contenidoSeccion}</ul>
                    </td>
                  </tr>
                </table>
              `;
            }
          } else {
            // Respuesta sin estructura de secciones
            let textoProcesado = respuestaTexto.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            textoProcesado = textoProcesado.replace(/\n/g, '<br>');
            htmlContent += `<div style="line-height: 1.6; margin: 15px 0;">${textoProcesado}</div>`;
          }
        }
      });
      
      // Agregar fotos si están disponibles
      if (fotos.length > 0 && !conversacionEspecifica) {
        htmlContent += `<h2 style="margin-top: 30px; color: #667eea;">📸 Fotos del Destino</h2>`;
        htmlContent += `<div class="pdf-photos-grid">`;
        
        const fotosParaPDF = fotos.slice(0, 3);
        fotosParaPDF.forEach((foto, index) => {
          htmlContent += `
            <div class="pdf-photo-item">
              <img src="${foto.url}" alt="${foto.descripcion || `Foto ${index + 1}`}" />
              ${foto.descripcion ? `<div class="pdf-photo-caption">${foto.descripcion}</div>` : ''}
            </div>
          `;
        });
        
        htmlContent += `</div>`;
      }
      
      pdfContainer.innerHTML = htmlContent;
      
      // Esperar a que las imágenes se carguen
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Convertir HTML a canvas y luego a PDF
      const canvas = await html2canvas(pdfContainer, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff'
      });
      
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgWidth = 210; // A4 width in mm
      const pageHeight = 297; // A4 height in mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      let heightLeft = imgHeight;
      let position = 0;
      
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
      
      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }
      
      // Limpiar
      document.body.removeChild(pdfContainer);
      
      // Guardar PDF
      const nombreArchivo = `ViajeIA_${destinoTexto.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
      pdf.save(nombreArchivo);
    } catch (error) {
      console.error('Error generando PDF:', error);
      alert('Hubo un error al generar el PDF. Por favor, intenta de nuevo.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setResponses([]);
    setClima(null);
    setFotos([]);
    setDestino(null);
    setInfoAdicional(null);
    setError('');

    try {
      // En producción (Vercel), usar rutas relativas. En desarrollo, usar la URL configurada o localhost
      const apiUrl = process.env.REACT_APP_API_URL || 
                     (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000');
      const res = await axios.post(`${apiUrl}/api/planificar`, {
        pregunta: question,
        session_id: sessionId
      });
      console.log('Respuesta del backend:', res.data);
      console.log('Clima recibido:', res.data.clima);
      console.log('Fotos recibidas:', res.data.fotos);
      console.log('Info adicional:', res.data.info_adicional);
      console.log('Destino:', res.data.destino);
      // Agregar nueva respuesta al array (primera respuesta desde formulario)
      setResponses([{
        pregunta: formData.destino ? `Quiero planear un viaje a ${formData.destino}` : '',
        respuesta: res.data.respuesta,
        esPrimera: true
      }]);
      setClima(res.data.clima || null);
      setFotos(res.data.fotos || []);
      setDestino(res.data.destino || null);
      setInfoAdicional(res.data.info_adicional || null);
      setHistorial(res.data.historial || []);
      
      // Debug: verificar qué se está guardando
      console.log('Estado actualizado - Clima:', res.data.clima);
      console.log('Estado actualizado - Fotos:', res.data.fotos?.length || 0);
      console.log('Estado actualizado - Info adicional:', res.data.info_adicional);
      console.log('Historial recibido:', res.data.historial);
      if (res.data.session_id) {
        setSessionId(res.data.session_id);
      }
    } catch (err) {
      console.error('Error:', err);
      const errorMessage = err.response?.data?.error || 
                          'Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestion('');
    setFollowUpQuestion('');
    setResponses([]);
    setClima(null);
    setFotos([]);
    setDestino(null);
    setSessionId(null);
    setInfoAdicional(null);
    setError('');
  };

  const handleFollowUpSubmit = async (e) => {
    e.preventDefault();
    if (!followUpQuestion.trim()) return;

    setLoading(true);
    setError('');

    try {
      // En producción (Vercel), usar rutas relativas. En desarrollo, usar la URL configurada o localhost
      const apiUrl = process.env.REACT_APP_API_URL || 
                     (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000');
      const res = await axios.post(`${apiUrl}/api/planificar`, {
        pregunta: followUpQuestion,
        session_id: sessionId
      });
      // Agregar nueva respuesta al array sin borrar las anteriores
      // IMPORTANTE: No actualizar clima, fotos, destino ni info adicional en preguntas de seguimiento
      // Solo agregar la nueva respuesta al chat
      setResponses(prev => {
        // Verificar que no estemos sobrescribiendo la primera respuesta
        const nuevaRespuesta = {
          pregunta: followUpQuestion,
          respuesta: res.data.respuesta,
          esPrimera: false
        };
        return [...prev, nuevaRespuesta];
      });
      
      // NO actualizar clima, fotos, destino ni info adicional - mantener los de la primera pregunta
      // Solo actualizar historial y session_id
      if (res.data.historial) setHistorial(res.data.historial);
      if (res.data.session_id) setSessionId(res.data.session_id);
      setFollowUpQuestion('');
    } catch (err) {
      console.error('Error:', err);
      const errorMessage = err.response?.data?.error || 
                          'Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    
    // Validar que todos los campos estén completos
    if (!formData.destino || !formData.fechaInicio || !formData.fechaFin || !formData.presupuesto || !formData.preferencia) {
      setError('Por favor, completa todos los campos del formulario');
      return;
    }

    // Construir pregunta inicial basada en el formulario
    const preguntaInicial = `Quiero planear un viaje a ${formData.destino} desde ${formData.fechaInicio} hasta ${formData.fechaFin}. Mi presupuesto aproximado es ${formData.presupuesto} y prefiero ${formData.preferencia}. ¿Puedes ayudarme a planificar este viaje?`;
    
    setQuestion(preguntaInicial);
    setShowForm(false);
    setError('');

    // Enviar automáticamente la pregunta
    setLoading(true);
    try {
      // En producción (Vercel), usar rutas relativas. En desarrollo, usar la URL configurada o localhost
      const apiUrl = process.env.REACT_APP_API_URL || 
                     (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000');
      const res = await axios.post(`${apiUrl}/api/planificar`, {
        pregunta: preguntaInicial
      });
      console.log('Respuesta del backend:', res.data);
      console.log('Clima recibido:', res.data.clima);
      console.log('Fotos recibidas:', res.data.fotos);
      console.log('Número de fotos:', res.data.fotos?.length || 0);
      console.log('Destino recibido:', res.data.destino);
      // Agregar nueva respuesta al array (primera respuesta desde formulario)
      setResponses([{
        pregunta: formData.destino ? `Quiero planear un viaje a ${formData.destino}` : '',
        respuesta: res.data.respuesta,
        esPrimera: true
      }]);
      setClima(res.data.clima || null);
      setFotos(res.data.fotos || []);
      setDestino(res.data.destino || null);
      setInfoAdicional(res.data.info_adicional || null);
    } catch (err) {
      console.error('Error:', err);
      const errorMessage = err.response?.data?.error || 
                          'Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleResetForm = () => {
    setShowForm(true);
    setFormData({
      destino: '',
      fechaInicio: '',
      fechaFin: '',
      presupuesto: '',
      preferencia: ''
    });
    setQuestion('');
    setFollowUpQuestion('');
    setResponses([]);
    setClima(null);
    setFotos([]);
    setDestino(null);
    setSessionId(null);
    setInfoAdicional(null);
    setError('');
  };

  return (
    <div className="App">
      {/* Panel Lateral con Información Actual y Favoritos */}
      <div className="sidebar-container">
        {/* Sección de Favoritos - Siempre visible si hay favoritos */}
        {favoritos.length > 0 && (
          <div className="favorites-sidebar fade-in">
            <div className="sidebar-header">
              <h3 className="sidebar-title">⭐ Mis Viajes Guardados</h3>
            </div>
            <div className="favorites-list">
              {favoritos.map((favorito, index) => (
                <div key={`favorito-${index}-${favorito.destino}`} className="favorite-item">
                  {favorito.fotos && favorito.fotos.length > 0 && (
                    <div className="favorite-photo">
                      <img
                        src={favorito.fotos[0].url_small || favorito.fotos[0].url}
                        alt={favorito.destino}
                        className="favorite-photo-image"
                      />
                    </div>
                  )}
                  <div className="favorite-content">
                    <div className="favorite-destination">{favorito.destino}</div>
                    {favorito.clima && (
                      <div className="favorite-weather">
                        {favorito.clima.temperatura}°C • {favorito.clima.descripcion}
                      </div>
                    )}
                    <div className="favorite-actions">
                      <button
                        className="favorite-load-btn"
                        onClick={() => handleCargarFavorito(favorito)}
                        title="Cargar este destino"
                      >
                        📍 Cargar
                      </button>
                      <button
                        className="favorite-delete-btn"
                        onClick={() => handleEliminarFavorito(favorito.destino)}
                        title="Eliminar de favoritos"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Panel Lateral con Información Actual - Mostrar si hay cualquier dato */}
        {((clima !== null) || (fotos.length > 0) || (infoAdicional !== null)) && (
          <div className="info-sidebar fade-in">
            <div className="sidebar-header">
              <h3 className="sidebar-title">ℹ️ Información de {destino || 'Destino'}</h3>
              {destino && !favoritos.some(fav => fav.destino.toLowerCase() === destino.toLowerCase()) && (
                <button
                  className="save-favorite-btn"
                  onClick={handleGuardarFavorito}
                  title="Guardar este destino en favoritos"
                >
                  ⭐ Guardar
                </button>
              )}
            </div>
          <div className="sidebar-content">
            {/* Debug info - remover en producción */}
            {console.log('Renderizando panel lateral - Clima:', clima, 'Fotos:', fotos.length, 'Info adicional:', infoAdicional)}
            {/* Fotos de Unsplash */}
            {fotos.length > 0 && (
              <div className="sidebar-photos">
                <div className="info-label" style={{marginBottom: '10px'}}>📸 Fotos del Destino</div>
                <div className="sidebar-photos-grid">
                  {fotos.map((foto, index) => (
                    <div key={index} className="sidebar-photo-item">
                      <img
                        src={foto.url_small || foto.url}
                        alt={foto.descripcion || `${destino || 'Destino'} - Foto ${index + 1}`}
                        className="sidebar-photo-image"
                        loading="lazy"
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Clima */}
            {clima && (
              <div className="info-item">
                <div className="info-icon">🌡️</div>
                <div className="info-details">
                  <div className="info-label">Temperatura Actual</div>
                  <div className="info-value">{clima.temperatura}°C</div>
                  <div className="info-subtext">{clima.descripcion} • {clima.ciudad}</div>
                </div>
              </div>
            )}
            
            {/* Hora Actual y Diferencia Horaria */}
            {infoAdicional?.diferencia_horaria && (() => {
              const utcOffset = infoAdicional.diferencia_horaria.utc_offset;
              // Parsear el offset (formato: +01:00 o -05:00)
              const offsetMatch = utcOffset.match(/([+-])(\d{2}):(\d{2})/);
              
              let horaDestino = horaActual;
              
              if (offsetMatch) {
                const sign = offsetMatch[1] === '+' ? 1 : -1;
                const hours = parseInt(offsetMatch[2]);
                const minutes = parseInt(offsetMatch[3]);
                const offsetMinutes = sign * (hours * 60 + minutes);
                
                // Obtener hora UTC actual
                const now = new Date();
                const utcTime = new Date(now.getTime() + (now.getTimezoneOffset() * 60 * 1000));
                // Aplicar offset del destino
                horaDestino = new Date(utcTime.getTime() + (offsetMinutes * 60 * 1000));
              }
              
              const horaFormateada = horaDestino.toLocaleTimeString('es-ES', { 
                hour: '2-digit', 
                minute: '2-digit',
                second: '2-digit'
              });
              
              // Calcular diferencia con hora local
              const horaLocal = horaActual.toLocaleTimeString('es-ES', { 
                hour: '2-digit', 
                minute: '2-digit'
              });
              
              // Calcular diferencia en horas
              const diffMs = horaDestino.getTime() - horaActual.getTime();
              const diffHours = Math.round(diffMs / (1000 * 60 * 60));
              const diffText = diffHours > 0 ? `+${diffHours}h` : `${diffHours}h`;
              
              return (
                <div className="info-item">
                  <div className="info-icon">🕐</div>
                  <div className="info-details">
                    <div className="info-label">Hora Actual</div>
                    <div className="info-value" style={{fontSize: '1.2rem', fontWeight: '700', fontFamily: 'monospace'}}>{horaFormateada}</div>
                    <div className="info-subtext">
                      {infoAdicional.diferencia_horaria.ciudad} • UTC{utcOffset}
                    </div>
                    <div className="info-subtext" style={{marginTop: '4px', fontSize: '0.75rem'}}>
                      Tu hora local: {horaLocal} ({diffText})
                    </div>
                  </div>
                </div>
              );
            })()}
            
            {/* Tipo de Cambio */}
            {infoAdicional?.tipo_cambio && (
              <div className="info-item">
                <div className="info-icon">💱</div>
                <div className="info-details">
                  <div className="info-label">Tipo de Cambio</div>
                  <div className="info-value">1 {infoAdicional.tipo_cambio.base} = {infoAdicional.tipo_cambio.rate} {infoAdicional.tipo_cambio.target}</div>
                  <div className="info-subtext">Actualizado hoy</div>
                </div>
              </div>
            )}
          </div>
        </div>
        )}
      </div>
      
      <div className="container">
        <header className="header">
          <h1 className="title">ViajeIA - Tu Asistente Personal de Viajes</h1>
          <p className="subtitle">Conoce a Axl 🧳, tu consultor personal de viajes. Pregúntame sobre destinos, itinerarios, presupuestos y más</p>
        </header>

        <main className="main-content">
          {showForm ? (
            <form onSubmit={handleFormSubmit} className="travel-form">
              <div className="form-header">
                <h2 className="form-title">🧳 Cuéntame sobre tu viaje</h2>
                <p className="form-subtitle">Completa este formulario rápido para que Axl pueda ayudarte mejor</p>
              </div>

              <div className="form-group">
                <label htmlFor="destino" className="form-label">
                  ¿A dónde quieres viajar? ✈️
                </label>
                <input
                  type="text"
                  id="destino"
                  className="form-input"
                  placeholder="Ej: París, Tokio, Cancún..."
                  value={formData.destino}
                  onChange={(e) => handleFormChange('destino', e.target.value)}
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="fechaInicio" className="form-label">
                    Fecha de inicio 📅
                  </label>
                  <input
                    type="date"
                    id="fechaInicio"
                    className="form-input"
                    value={formData.fechaInicio}
                    onChange={(e) => handleFormChange('fechaInicio', e.target.value)}
                    min={new Date().toISOString().split('T')[0]}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="fechaFin" className="form-label">
                    Fecha de regreso 📅
                  </label>
                  <input
                    type="date"
                    id="fechaFin"
                    className="form-input"
                    value={formData.fechaFin}
                    onChange={(e) => handleFormChange('fechaFin', e.target.value)}
                    min={formData.fechaInicio || new Date().toISOString().split('T')[0]}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="presupuesto" className="form-label">
                  ¿Cuál es tu presupuesto aproximado? 💰
                </label>
                <select
                  id="presupuesto"
                  className="form-select"
                  value={formData.presupuesto}
                  onChange={(e) => handleFormChange('presupuesto', e.target.value)}
                  required
                >
                  <option value="">Selecciona un rango</option>
                  <option value="Económico (menos de $500 USD)">Económico (menos de $500 USD)</option>
                  <option value="Moderado ($500 - $1,500 USD)">Moderado ($500 - $1,500 USD)</option>
                  <option value="Comfortable ($1,500 - $3,000 USD)">Comfortable ($1,500 - $3,000 USD)</option>
                  <option value="Lujo (más de $3,000 USD)">Lujo (más de $3,000 USD)</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">
                  ¿Qué tipo de experiencia prefieres? 🎯
                </label>
                <div className="preference-buttons">
                  <button
                    type="button"
                    className={`preference-btn ${formData.preferencia === 'aventura' ? 'active' : ''}`}
                    onClick={() => handleFormChange('preferencia', 'aventura')}
                  >
                    🏔️ Aventura
                  </button>
                  <button
                    type="button"
                    className={`preference-btn ${formData.preferencia === 'relajación' ? 'active' : ''}`}
                    onClick={() => handleFormChange('preferencia', 'relajación')}
                  >
                    🏖️ Relajación
                  </button>
                  <button
                    type="button"
                    className={`preference-btn ${formData.preferencia === 'cultura' ? 'active' : ''}`}
                    onClick={() => handleFormChange('preferencia', 'cultura')}
                  >
                    🏛️ Cultura
                  </button>
                </div>
              </div>

              <button type="submit" className="form-submit-button">
                🚀 Planificar mi viaje con Axl
              </button>
            </form>
          ) : (
            <>
              <div className="form-summary">
                <div className="summary-content">
                  <span className="summary-label">Destino:</span>
                  <span className="summary-value">{formData.destino}</span>
                  <span className="summary-label">Fechas:</span>
                  <span className="summary-value">
                    {new Date(formData.fechaInicio).toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })} - {new Date(formData.fechaFin).toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })}
                  </span>
                  <span className="summary-label">Presupuesto:</span>
                  <span className="summary-value">{formData.presupuesto}</span>
                  <span className="summary-label">Preferencia:</span>
                  <span className="summary-value">
                    {formData.preferencia.charAt(0).toUpperCase() + formData.preferencia.slice(1)}
                  </span>
                </div>
                <button
                  type="button"
                  className="reset-form-button"
                  onClick={handleResetForm}
                >
                  ✏️ Cambiar información
                </button>
              </div>

              <form onSubmit={handleSubmit} className="question-form">
            <div className="input-group">
              <textarea
                className="question-input"
                placeholder="Ejemplo: ¿Qué lugares debo visitar en París en 3 días?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows="4"
                disabled={loading}
              />
              {question && !loading && (
                <button
                  type="button"
                  className="clear-button"
                  onClick={handleClear}
                  aria-label="Limpiar"
                >
                  ✕
                </button>
              )}
            </div>
            <button
              type="submit"
              className="submit-button"
              disabled={loading || !question.trim()}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  <span>Planificando tu viaje...</span>
                </>
              ) : (
                'Planificar mi viaje'
              )}
            </button>
          </form>

          {loading && (
            <div className="loading-area">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <p className="loading-text">Axl está preparando tu plan de viaje... ✈️</p>
            </div>
          )}

          {error && (
            <div className="error-area">
              <div className="error-icon">⚠️</div>
              <div className="error-content">
                <h3 className="error-title">Error</h3>
                <p className="error-message">{error}</p>
              </div>
            </div>
          )}

          {responses.length > 0 && !loading && (
            <>
              {/* Panel de Clima con Fotos - Solo mostrar en la primera respuesta */}
              {responses[0]?.esPrimera && (clima || fotos.length > 0) && (
                <div className="weather-panel fade-in">
                  {clima && (
                    <>
                      <div className="weather-header">
                        <h3 className="weather-title">🌤️ Clima Actual en {clima.ciudad}</h3>
                      </div>
                      <div className="weather-content">
                        <div className="weather-main">
                          <div className="weather-temp">
                            {clima.temperatura}°C
                          </div>
                          <div className="weather-desc">
                            {clima.descripcion}
                          </div>
                        </div>
                        <div className="weather-details">
                          <div className="weather-item">
                            <span className="weather-label">Sensación térmica:</span>
                            <span className="weather-value">{clima.sensacion_termica}°C</span>
                          </div>
                          <div className="weather-item">
                            <span className="weather-label">Humedad:</span>
                            <span className="weather-value">{clima.humedad}%</span>
                          </div>
                          <div className="weather-item">
                            <span className="weather-label">Viento:</span>
                            <span className="weather-value">{clima.viento} m/s</span>
                          </div>
                        </div>
                      </div>
                    </>
                  )}
                  
                  {/* Fotos dentro del mismo panel */}
                  {fotos.length > 0 && (
                    <div className="photos-section">
                      <h3 className="photos-title">📸 {destino || 'Destino'}</h3>
                      <div className="photos-grid">
                        {fotos.map((foto, index) => (
                          <div key={index} className="photo-item">
                            <img
                              src={foto.url}
                              alt={foto.descripcion || `${destino || 'Destino'} - Foto ${index + 1}`}
                              className="photo-image"
                              loading="lazy"
                            />
                            <div className="photo-overlay">
                              <a
                                href={foto.autor_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="photo-credit"
                              >
                                Foto por {foto.autor}
                              </a>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Chat de Respuestas - Mostrar todas acumuladas */}
              <div className="chat-container">
                {responses.map((item, index) => {
                  // Key estable: para la primera respuesta usar un hash simple del contenido
                  // para las siguientes usar índice + pregunta (más estable que Date.now())
                  const stableKey = item.esPrimera 
                    ? `first-response-fixed-${item.respuesta.substring(0, 50).replace(/\s/g, '-')}`
                    : `follow-${index}-${item.pregunta?.substring(0, 15).replace(/\s/g, '-') || index}`;
                  
                  return (
                    <div 
                      key={stableKey}
                      className="response-area fade-in"
                    >
                      {item.pregunta && (
                        <div className="user-question">
                          <div className="question-bubble">
                            <strong>Tu pregunta:</strong> {item.pregunta}
                          </div>
                        </div>
                      )}
                      <div className="response-header">
                        <h2 className="response-title">Respuesta de Axl 🧳</h2>
                        <div className="response-header-actions">
                          {index === 0 && responses.length > 0 && (
                            <button
                              className="download-pdf-button"
                              onClick={() => generarPDF()}
                              title="Descargar mi itinerario en PDF"
                            >
                              📥 Descargar PDF
                            </button>
                          )}
                          {index === 0 && (
                            <button
                              className="close-button"
                              onClick={() => {
                                setResponses([]);
                                setClima(null);
                                setFotos([]);
                                setDestino(null);
                                setSessionId(null);
                                setInfoAdicional(null);
                                setHistorial([]);
                                setFollowUpQuestion('');
                              }}
                              aria-label="Cerrar chat"
                            >
                              ✕
                            </button>
                          )}
                        </div>
                      </div>
                      <div className="response-content">
                        {renderMarkdown(item.respuesta)}
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Historial de Conversación */}
              {historial.length > 0 && (
                <div className="history-panel fade-in">
                  <div className="history-header">
                    <h3 className="history-title">📜 Historial de Conversación</h3>
                    <span className="history-count">{historial.length} {historial.length === 1 ? 'pregunta' : 'preguntas'}</span>
                  </div>
                  <div className="history-list">
                    {historial.map((item, index) => (
                      <div key={index} className="history-item">
                        <div className="history-content">
                          <div className="history-question">
                            <span className="history-icon">❓</span>
                            <span className="history-text">{item.pregunta}</span>
                          </div>
                          {item.respuesta && (
                            <div className="history-answer">
                              <span className="history-icon">💬</span>
                              <span className="history-text">{item.respuesta}</span>
                            </div>
                          )}
                        </div>
                        <button
                          className="history-download-btn"
                          onClick={() => generarPDF({ pregunta: item.pregunta, respuesta: item.respuesta })}
                          title="Descargar esta conversación en PDF"
                        >
                          📥
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Área de Preguntas de Seguimiento - Solo mostrar si hay respuestas */}
              {responses.length > 0 && (
                <div className="follow-up-area fade-in">
                  <h3 className="follow-up-title">💬 ¿Tienes más preguntas sobre {destino || 'este destino'}?</h3>
                <p className="follow-up-subtitle">Pregúntale a Axl cualquier cosa adicional sobre el viaje</p>
                <form onSubmit={handleFollowUpSubmit} className="follow-up-form">
                  <div className="input-group">
                    <textarea
                      className="question-input"
                      placeholder="Ejemplo: ¿Qué transporte público recomiendas? ¿Hay algún festival durante mi visita?"
                      value={followUpQuestion}
                      onChange={(e) => setFollowUpQuestion(e.target.value)}
                      rows="3"
                      disabled={loading}
                    />
                  </div>
                  <button
                    type="submit"
                    className="submit-button"
                    disabled={loading || !followUpQuestion.trim()}
                  >
                    {loading ? (
                      <>
                        <span className="spinner"></span>
                        <span>Preguntando a Axl...</span>
                      </>
                    ) : (
                      'Hacer pregunta de seguimiento'
                    )}
                  </button>
                </form>
                </div>
              )}
            </>
          )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;

