import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  TextInput,
  Alert,
  Modal,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '../contexts/AuthContext';
import { questionService } from '../services/api';

interface Question {
  question_id: string;
  question_number?: number;
  content: string;
  answer: string;
  type: string;
  category_name?: string;
  options?: string[];
  difficulty?: string;
  explanation?: string;
}

export default function AdminQuestions() {
  const router = useRouter();
  const { sessionToken } = useAuth();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [filteredQuestions, setFilteredQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, []);

  useEffect(() => {
    filterQuestions();
  }, [searchQuery, filterType, questions]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      const data = await questionService.getQuestions(undefined, undefined, sessionToken || undefined);
      setQuestions(data);
    } catch (error) {
      console.error('Failed to load questions:', error);
      Alert.alert('Error', 'Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const filterQuestions = () => {
    let filtered = questions;

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(q => q.type === filterType);
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(q =>
        q.content.toLowerCase().includes(query) ||
        q.answer.toLowerCase().includes(query) ||
        (q.category_name || '').toLowerCase().includes(query)
      );
    }

    setFilteredQuestions(filtered);
  };

  const handleEdit = (question: Question) => {
    setEditingQuestion({...question});
    setShowEditModal(true);
  };

  const handleSaveEdit = async () => {
    if (!editingQuestion) return;

    try {
      await questionService.updateQuestion(
        editingQuestion.question_id,
        {
          content: editingQuestion.content,
          answer: editingQuestion.answer,
          explanation: editingQuestion.explanation,
          difficulty: editingQuestion.difficulty,
          options: editingQuestion.options,
        },
        sessionToken || undefined
      );

      Alert.alert('Success', 'Question updated successfully');
      setShowEditModal(false);
      loadQuestions();
    } catch (error) {
      console.error('Failed to update question:', error);
      Alert.alert('Error', 'Failed to update question');
    }
  };

  const handleDelete = (question: Question) => {
    Alert.alert(
      'Delete Question',
      `Are you sure you want to delete this question?\n\n"${question.content.substring(0, 100)}..."`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await questionService.deleteQuestion(question.question_id, sessionToken || undefined);
              Alert.alert('Success', 'Question deleted');
              loadQuestions();
            } catch (error) {
              console.error('Failed to delete:', error);
              Alert.alert('Error', 'Failed to delete question');
            }
          },
        },
      ]
    );
  };

  const TypeBadge = ({ type }: { type: string }) => {
    const colors: any = {
      flashcard: '#3b82f6',
      scenario: '#10b981',
      multiple_choice: '#f59e0b',
    };
    return (
      <View style={[styles.typeBadge, { backgroundColor: colors[type] || '#6b7280' }]}>
        <Text style={styles.typeBadgeText}>{type.replace('_', ' ')}</Text>
      </View>
    );
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#2563eb" />
          <Text style={styles.loadingText}>Loading questions...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Manage Questions</Text>
        <View style={styles.backButton} />
      </View>

      {/* Search and Filters */}
      <View style={styles.filtersContainer}>
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#64748b" />
          <TextInput
            style={styles.searchInput}
            placeholder="Search questions..."
            placeholderTextColor="#64748b"
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
          {searchQuery ? (
            <TouchableOpacity onPress={() => setSearchQuery('')}>
              <Ionicons name="close-circle" size={20} color="#64748b" />
            </TouchableOpacity>
          ) : null}
        </View>

        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.typeFilters}>
          {['all', 'flashcard', 'scenario', 'multiple_choice'].map(type => (
            <TouchableOpacity
              key={type}
              style={[styles.filterButton, filterType === type && styles.filterButtonActive]}
              onPress={() => setFilterType(type)}
            >
              <Text style={[styles.filterButtonText, filterType === type && styles.filterButtonTextActive]}>
                {type === 'all' ? 'All' : type.replace('_', ' ')}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        <Text style={styles.resultCount}>
          {filteredQuestions.length} of {questions.length} questions
        </Text>
      </View>

      {/* Questions List */}
      <ScrollView style={styles.scrollView}>
        {filteredQuestions.map((question, index) => (
          <View key={question.question_id} style={styles.questionCard}>
            <View style={styles.questionHeader}>
              <TypeBadge type={question.type} />
              <Text style={styles.questionNumber}>
                #{question.question_number || index + 1}
              </Text>
            </View>

            <Text style={styles.questionContent} numberOfLines={3}>
              {question.content}
            </Text>

            <View style={styles.answerContainer}>
              <Text style={styles.answerLabel}>Answer:</Text>
              <Text style={styles.answerText} numberOfLines={2}>
                {question.answer}
              </Text>
            </View>

            {question.category_name && (
              <Text style={styles.categoryText}>📁 {question.category_name}</Text>
            )}

            <View style={styles.actionButtons}>
              <TouchableOpacity
                style={styles.editButton}
                onPress={() => handleEdit(question)}
              >
                <Ionicons name="pencil" size={18} color="#fff" />
                <Text style={styles.editButtonText}>Edit</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.deleteButton}
                onPress={() => handleDelete(question)}
              >
                <Ionicons name="trash" size={18} color="#fff" />
                <Text style={styles.deleteButtonText}>Delete</Text>
              </TouchableOpacity>
            </View>
          </View>
        ))}

        {filteredQuestions.length === 0 && (
          <View style={styles.emptyState}>
            <Ionicons name="search-outline" size={64} color="#334155" />
            <Text style={styles.emptyText}>No questions found</Text>
            <Text style={styles.emptySubText}>Try adjusting your search or filters</Text>
          </View>
        )}
      </ScrollView>

      {/* Edit Modal */}
      <Modal
        visible={showEditModal}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <SafeAreaView style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <TouchableOpacity onPress={() => setShowEditModal(false)}>
              <Text style={styles.cancelText}>Cancel</Text>
            </TouchableOpacity>
            <Text style={styles.modalTitle}>Edit Question</Text>
            <TouchableOpacity onPress={handleSaveEdit}>
              <Text style={styles.saveText}>Save</Text>
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.modalContent}>
            {editingQuestion && (
              <>
                <View style={styles.formGroup}>
                  <Text style={styles.label}>Question:</Text>
                  <TextInput
                    style={[styles.input, styles.textArea]}
                    value={editingQuestion.content}
                    onChangeText={(text) => setEditingQuestion({...editingQuestion, content: text})}
                    multiline
                    numberOfLines={4}
                    placeholderTextColor="#64748b"
                  />
                </View>

                <View style={styles.formGroup}>
                  <Text style={styles.label}>Answer:</Text>
                  <TextInput
                    style={[styles.input, styles.textArea]}
                    value={editingQuestion.answer}
                    onChangeText={(text) => setEditingQuestion({...editingQuestion, answer: text})}
                    multiline
                    numberOfLines={4}
                    placeholderTextColor="#64748b"
                  />
                </View>

                <View style={styles.formGroup}>
                  <Text style={styles.label}>Explanation (optional):</Text>
                  <TextInput
                    style={[styles.input, styles.textArea]}
                    value={editingQuestion.explanation || ''}
                    onChangeText={(text) => setEditingQuestion({...editingQuestion, explanation: text})}
                    multiline
                    numberOfLines={3}
                    placeholder="Add explanation..."
                    placeholderTextColor="#64748b"
                  />
                </View>

                <View style={styles.formGroup}>
                  <Text style={styles.label}>Difficulty:</Text>
                  <View style={styles.difficultyButtons}>
                    {['easy', 'medium', 'hard'].map(diff => (
                      <TouchableOpacity
                        key={diff}
                        style={[
                          styles.difficultyButton,
                          editingQuestion.difficulty === diff && styles.difficultyButtonActive
                        ]}
                        onPress={() => setEditingQuestion({...editingQuestion, difficulty: diff})}
                      >
                        <Text style={[
                          styles.difficultyButtonText,
                          editingQuestion.difficulty === diff && styles.difficultyButtonTextActive
                        ]}>
                          {diff}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </View>

                {editingQuestion.type === 'multiple_choice' && (
                  <View style={styles.formGroup}>
                    <Text style={styles.label}>Options (one per line):</Text>
                    <TextInput
                      style={[styles.input, styles.textArea]}
                      value={(editingQuestion.options || []).join('\n')}
                      onChangeText={(text) => setEditingQuestion({
                        ...editingQuestion,
                        options: text.split('\n').filter(o => o.trim())
                      })}
                      multiline
                      numberOfLines={6}
                      placeholder="Option 1\nOption 2\nOption 3\nOption 4"
                      placeholderTextColor="#64748b"
                    />
                  </View>
                )}
              </>
            )}
          </ScrollView>
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  backButton: {
    padding: 8,
    width: 40,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 16,
  },
  loadingText: {
    color: '#94a3b8',
    fontSize: 16,
  },
  filtersContainer: {
    padding: 16,
    gap: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 12,
  },
  searchInput: {
    flex: 1,
    color: '#fff',
    fontSize: 16,
  },
  typeFilters: {
    flexDirection: 'row',
  },
  filterButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#1e293b',
    marginRight: 8,
  },
  filterButtonActive: {
    backgroundColor: '#2563eb',
  },
  filterButtonText: {
    color: '#94a3b8',
    fontSize: 14,
    fontWeight: '500',
    textTransform: 'capitalize',
  },
  filterButtonTextActive: {
    color: '#fff',
  },
  resultCount: {
    color: '#64748b',
    fontSize: 14,
  },
  scrollView: {
    flex: 1,
  },
  questionCard: {
    backgroundColor: '#1e293b',
    margin: 16,
    marginBottom: 8,
    padding: 16,
    borderRadius: 12,
    gap: 12,
  },
  questionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  typeBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  typeBadgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  questionNumber: {
    color: '#64748b',
    fontSize: 14,
  },
  questionContent: {
    color: '#fff',
    fontSize: 16,
    lineHeight: 24,
  },
  answerContainer: {
    backgroundColor: '#0f172a',
    padding: 12,
    borderRadius: 8,
  },
  answerLabel: {
    color: '#64748b',
    fontSize: 12,
    marginBottom: 4,
  },
  answerText: {
    color: '#10b981',
    fontSize: 14,
    lineHeight: 20,
  },
  categoryText: {
    color: '#94a3b8',
    fontSize: 13,
  },
  actionButtons: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 8,
  },
  editButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#2563eb',
    paddingVertical: 10,
    borderRadius: 8,
  },
  editButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  deleteButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#dc2626',
    paddingVertical: 10,
    borderRadius: 8,
  },
  deleteButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 48,
    gap: 12,
  },
  emptyText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  emptySubText: {
    color: '#64748b',
    fontSize: 14,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: '#0c0c0c',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  cancelText: {
    color: '#ef4444',
    fontSize: 16,
  },
  saveText: {
    color: '#10b981',
    fontSize: 16,
    fontWeight: '600',
  },
  modalContent: {
    flex: 1,
    padding: 16,
  },
  formGroup: {
    marginBottom: 24,
  },
  label: {
    color: '#cbd5e1',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#1e293b',
    borderRadius: 8,
    padding: 12,
    color: '#fff',
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  textArea: {
    minHeight: 100,
    textAlignVertical: 'top',
  },
  difficultyButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  difficultyButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 8,
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#334155',
    alignItems: 'center',
  },
  difficultyButtonActive: {
    backgroundColor: '#2563eb',
    borderColor: '#2563eb',
  },
  difficultyButtonText: {
    color: '#94a3b8',
    fontSize: 14,
    fontWeight: '500',
    textTransform: 'capitalize',
  },
  difficultyButtonTextActive: {
    color: '#fff',
    fontWeight: '600',
  },
});
// Deploy trigger
// Numbers
