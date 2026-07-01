import { StyleSheet, Text, View } from "react-native";

type ResultCardProps = {
  analysis: any;
};

export default function ResultCard({ analysis }: ResultCardProps) {
  if (!analysis) return null;

  return (
    <View style={styles.card}>
      <Text style={styles.mainTitle}>Analysis Result</Text>

      <Text style={styles.sectionTitle}>Candidate Summary</Text>
      <Text style={styles.text}>{analysis.candidate_summary}</Text>

      <Text style={styles.sectionTitle}>Key Skills</Text>
      <View style={styles.tagContainer}>
        {analysis.key_skills?.map((skill: string, index: number) => (
          <View key={index} style={styles.tag}>
            <Text style={styles.tagText}>{skill}</Text>
          </View>
        ))}
      </View>

      <Text style={styles.sectionTitle}>Work Experience</Text>

      {Array.isArray(analysis.work_experience) &&
        analysis.work_experience.map((job: any, index: number) => (
          <View key={index} style={styles.subCard}>
            <Text style={styles.subCardTitle}>
              {job.position || job.title || "Experience"}
            </Text>

            <Text style={styles.subCardMeta}>
              {job.company ? `${job.company}` : ""}
              {job.dates ? ` • ${job.dates}` : ""}
            </Text>

            {Array.isArray(job.responsibilities) ? (
              job.responsibilities.map((item: string, itemIndex: number) => (
                <Text key={itemIndex} style={styles.listItem}>
                  • {item}
                </Text>
              ))
            ) : job.responsibilities ? (
              <Text style={styles.listItem}>• {job.responsibilities}</Text>
            ) : null}

            {job.description ? (
              <Text style={styles.text}>{job.description}</Text>
            ) : null}
          </View>
        ))}

      <Text style={styles.sectionTitle}>Education</Text>
      {analysis.education?.map((edu: any, index: number) => (
        <View key={index} style={styles.subCard}>
          <Text style={styles.subCardTitle}>
            {edu.degree || edu.program || edu.title || "Education"}
          </Text>

          <Text style={styles.subCardMeta}>
            {edu.institution || edu.university || ""}
            {edu.dates ? ` • ${edu.dates}` : ""}
          </Text>
        </View>
      ))}

      <Text style={styles.sectionTitle}>Recommended Roles</Text>
      {analysis.recommended_roles?.map((role: string, index: number) => (
        <Text key={index} style={styles.listItem}>
          • {role}
        </Text>
      ))}

      <Text style={styles.sectionTitle}>Strengths</Text>
      {analysis.strengths?.map((item: string, index: number) => (
        <Text key={index} style={styles.listItem}>
          • {item}
        </Text>
      ))}

      <Text style={styles.sectionTitle}>Concerns / Missing Info</Text>
      {analysis.concerns_or_missing_info?.map((item: string, index: number) => (
        <Text key={index} style={styles.listItem}>
          • {item}
        </Text>
      ))}

      <Text style={styles.sectionTitle}>HR Recommendation</Text>
      <View style={styles.recommendationBox}>
        <Text style={styles.recommendationText}>
          {analysis.hr_recommendation}
        </Text>
      </View>

      <Text style={styles.sectionTitle}>English Summary</Text>
      <Text style={styles.text}>{analysis.english_summary}</Text>

      <Text style={styles.sectionTitle}>Chinese Summary</Text>
      <Text style={styles.text}>{analysis.chinese_summary}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    width: "100%",
    marginTop: 32,
    backgroundColor: "#FFFFFF",
    borderRadius: 26,
    padding: 26,
    borderWidth: 1,
    borderColor: "#E9D5FF",
    shadowColor: "#6D28D9",
    shadowOpacity: 0.08,
    shadowRadius: 20,
    shadowOffset: { width: 0, height: 10 },
    elevation: 3,
  },
  mainTitle: {
    fontSize: 24,
    fontWeight: "900",
    color: "#4C1D95",
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: "900",
    color: "#111827",
    marginTop: 22,
    marginBottom: 9,
  },
  text: {
    fontSize: 14,
    lineHeight: 22,
    color: "#374151",
  },
  tagContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },
  tag: {
    backgroundColor: "#EDE9FE",
    paddingHorizontal: 11,
    paddingVertical: 7,
    borderRadius: 999,
    marginBottom: 6,
  },
  tagText: {
    fontSize: 13,
    color: "#5B21B6",
    fontWeight: "800",
  },
  listItem: {
    fontSize: 14,
    lineHeight: 23,
    color: "#374151",
    marginBottom: 3,
  },
  subCard: {
    backgroundColor: "#FAFAFF",
    borderWidth: 1,
    borderColor: "#EDE9FE",
    borderRadius: 18,
    padding: 16,
    marginBottom: 10,
  },
  subCardTitle: {
    fontSize: 15,
    fontWeight: "800",
    color: "#111827",
    marginBottom: 4,
  },
  subCardMeta: {
    fontSize: 13,
    color: "#6B7280",
    marginBottom: 8,
  },
  recommendationBox: {
    backgroundColor: "#F5F3FF",
    borderLeftWidth: 4,
    borderLeftColor: "#6D28D9",
    borderRadius: 16,
    padding: 16,
  },
  recommendationText: {
    fontSize: 14,
    lineHeight: 22,
    color: "#312E81",
    fontWeight: "600",
  },
});
