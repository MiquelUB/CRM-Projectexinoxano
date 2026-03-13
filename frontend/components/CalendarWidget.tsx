"use client";

import { useState } from "react";
import { 
  format, 
  startOfMonth, 
  endOfMonth, 
  startOfWeek, 
  endOfWeek, 
  eachDayOfInterval, 
  isSameMonth, 
  isSameDay, 
  addMonths, 
  subMonths 
} from "date-fns";
import { ca } from "date-fns/locale";
import { ChevronLeft, ChevronRight, Circle, Phone, Mail, MonitorPlay, MessageSquare, Calendar as CalendarIcon, Clock } from "lucide-react";

interface CalendarWidgetProps {
  tasques: any[];
  onSelectDate?: (date: Date) => void;
  onNewTask?: (date: Date) => void;
  onSelectTask?: (task: any) => void;
}

export function CalendarWidget({ tasques, onSelectDate, onNewTask, onSelectTask }: CalendarWidgetProps) {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(new Date());

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(monthStart);
  const startDate = startOfWeek(monthStart, { weekStartsOn: 1 });
  const endDate = endOfWeek(monthEnd, { weekStartsOn: 1 });

  const days = eachDayOfInterval({ start: startDate, end: endDate });

  const nextMonth = () => setCurrentMonth(addMonths(currentMonth, 1));
  const prevMonth = () => setCurrentMonth(subMonths(currentMonth, 1));

  const getTasquesForDay = (day: Date) => {
    return tasques.filter(t => isSameDay(new Date(t.data_venciment), day));
  };

  const getDayIcon = (type: string) => {
    switch (type) {
      case 'trucada': return <Phone className="w-3 h-3" />;
      case 'email': return <Mail className="w-3 h-3" />;
      case 'demo': return <MonitorPlay className="w-3 h-3" />;
      case 'reunio': return <MessageSquare className="w-3 h-3" />;
      default: return <Circle className="w-2 h-2 fill-current" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'trucada': return 'text-blue-500';
      case 'email': return 'text-indigo-500';
      case 'demo': return 'text-emerald-500';
      case 'reunio': return 'text-amber-500';
      default: return 'text-slate-400';
    }
  };

  const selectedDayTasques = getTasquesForDay(selectedDate);

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
      {/* Calendari Grid */}
      <div className="bg-white/80 backdrop-blur-md border border-white/60 rounded-3xl p-6 shadow-xl shadow-slate-200/40">
        <div className="flex items-center justify-between mb-8 px-2">
          <h2 className="text-lg font-black text-slate-800 uppercase tracking-tight">
            {format(currentMonth, 'MMMM yyyy', { locale: ca })}
          </h2>
          <div className="flex space-x-2">
            <button onClick={prevMonth} className="p-2 hover:bg-slate-100 rounded-xl transition-all">
              <ChevronLeft className="w-5 h-5 text-slate-400" />
            </button>
            <button onClick={nextMonth} className="p-2 hover:bg-slate-100 rounded-xl transition-all">
              <ChevronRight className="w-5 h-5 text-slate-400" />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-7 gap-1">
          {['dl', 'dt', 'dm', 'dj', 'dv', 'ds', 'dg'].map(d => (
            <div key={d} className="text-center text-[10px] font-black text-slate-300 uppercase tracking-widest pb-4">
              {d}
            </div>
          ))}
          {days.map((day, idx) => {
            const dayTasques = getTasquesForDay(day);
            const isSelected = isSameDay(day, selectedDate);
            const isCurrentMonth = isSameMonth(day, monthStart);
            const isToday = isSameDay(day, new Date());

            return (
              <button
                key={idx}
                onClick={() => {
                   setSelectedDate(day);
                   if (onSelectDate) onSelectDate(day);
                }}
                className={`relative aspect-square rounded-2xl flex flex-col items-center justify-center transition-all ${
                  isSelected 
                  ? "bg-slate-900 text-white shadow-lg shadow-slate-200" 
                  : isToday 
                    ? "bg-blue-50 text-blue-600 font-black border border-blue-100" 
                    : isCurrentMonth 
                      ? "hover:bg-slate-50 text-slate-600 font-bold" 
                      : "text-slate-200 font-medium"
                }`}
              >
                <span className="text-sm">{format(day, 'd')}</span>
                {dayTasques.length > 0 && (
                  <div className="absolute bottom-2 flex space-x-0.5">
                    {dayTasques.slice(0, 3).map((t, i) => (
                      <div 
                        key={i} 
                        className={`w-1 h-1 rounded-full ${isSelected ? 'bg-white/60' : getTypeColor(t.tipus).replace('text-', 'bg-')}`} 
                      />
                    ))}
                  </div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Llista de Tasques del Dia */}
      <div className="flex flex-col h-full space-y-6">
        <div className="flex items-center space-x-3 mb-2">
           <div className="w-12 h-12 bg-white border border-slate-100 rounded-2xl flex flex-col items-center justify-center shadow-sm">
              <span className="text-[10px] font-black text-slate-400 uppercase leading-none">{format(selectedDate, 'MMM', { locale: ca })}</span>
              <span className="text-xl font-black text-slate-800 leading-none mt-1">{format(selectedDate, 'd')}</span>
           </div>
           <div>
              <h3 className="text-xl font-black text-slate-800 tracking-tight">Agenda d'avui</h3>
              <p className="text-xs font-medium text-slate-400">Tens {selectedDayTasques.length} tasca(es) per a aquest dia.</p>
           </div>
        </div>

        <div className="flex-1 space-y-4 overflow-y-auto max-h-[400px] pr-2 custom-scrollbar">
          {selectedDayTasques.length > 0 ? (
            selectedDayTasques.map((t) => (
              <div 
                key={t.id} 
                onClick={() => onSelectTask && onSelectTask(t)}
                className="p-5 bg-white border border-slate-100 rounded-3xl flex items-start space-x-4 shadow-sm hover:shadow-md hover:border-blue-200 transition-all group cursor-pointer"
              >
                <div className={`w-12 h-12 flex-shrink-0 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform ${getTypeColor(t.tipus).replace('text-', 'bg-').replace('-500', '-50')} ${getTypeColor(t.tipus)}`}>
                   {getDayIcon(t.tipus)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-[10px] font-black uppercase tracking-widest ${getTypeColor(t.tipus)}`}>{t.tipus}</span>
                    <div className="flex items-center text-[10px] font-bold text-slate-400 space-x-1">
                       <Clock className="w-3 h-3" />
                       <span>{t.prioritat?.toUpperCase()}</span>
                    </div>
                  </div>
                  <h4 className="text-sm font-black text-slate-800 truncate">{t.titol}</h4>
                  
                  <div className="mt-2 space-y-1">
                    {t.entitat_nom && (
                      <div className="flex items-center text-[10px] font-bold text-slate-500 uppercase tracking-tighter">
                        <span className="text-blue-500 mr-1 opacity-70">Ajuntament:</span>
                        <span className="truncate">{t.entitat_nom}</span>
                      </div>
                    )}
                    {t.contacte_nom && (
                      <div className="flex items-center text-[10px] font-bold text-slate-500 uppercase tracking-tighter">
                        <span className="text-indigo-500 mr-1 opacity-70">Persona:</span>
                        <span className="truncate">{t.contacte_nom}</span>
                      </div>
                    )}
                  </div>

                  {t.descripcio && (
                    <p className="text-[11px] text-slate-400 mt-2 leading-relaxed line-clamp-2 italic">
                      {t.descripcio}
                    </p>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center py-10 opacity-40">
              <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center text-2xl mb-4">🧘</div>
              <p className="text-sm text-slate-500 font-bold uppercase tracking-widest">Cap tasca en agenda</p>
              <p className="text-xs text-slate-400 mt-1 italic">Gaudeix d'un moment de tranquil·litat o planifica accions.</p>
            </div>
          )}
        </div>

        <button 
          onClick={() => onNewTask && onNewTask(selectedDate)}
          className="w-full h-14 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-2xl font-black text-xs uppercase tracking-widest transition-all flex items-center justify-center space-x-2 border border-slate-200/50"
        >
           <CalendarIcon className="w-4 h-4" />
           <span>Nova Tasca d'Agenda</span>
        </button>
      </div>
    </div>
  );
}
